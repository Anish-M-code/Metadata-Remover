#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <qmessagebox.h>
#include <windows.h>
#include <QDesktopServices>
#include <QUrl>
#include <QProcess>
#include <QTextStream>
#include <QDebug>
#include <QDir>
#include <QTimer>
#include <QFileInfo>
#include <QFileDialog>
#include <QFutureWatcher>
#include <QtConcurrent/QtConcurrent>
#include "downloadprogress.h"

QString getFileNameFromPath(const QString &absolutePath) {
    QFileInfo fileInfo(absolutePath);
    return fileInfo.fileName();  // Returns just the filename (with extension)
}

bool copyFolder(const QString &sourcePath, const QString &destinationPath) {
    QDir sourceDir(sourcePath);
    if (!sourceDir.exists()) {
        qWarning() << "Source directory does not exist:" << sourcePath;
        return false;
    }

    QDir destinationDir(destinationPath);
    if (!destinationDir.exists()) {
        if (!destinationDir.mkpath(".")) {
            qWarning() << "Failed to create destination directory:" << destinationPath;
            return false;
        }
    }
    else{
        destinationDir.removeRecursively();
    }

    foreach (const QString &file, sourceDir.entryList(QDir::Files | QDir::NoDotAndDotDot)) {
        QString sourceFilePath = sourceDir.filePath(file);
        QString destinationFilePath = destinationDir.filePath(file);
        if (!QFile::copy(sourceFilePath, destinationFilePath)) {
            qWarning() << "Failed to copy file:" << sourceFilePath;
            return false;
        }
    }

    foreach (const QString &subDir, sourceDir.entryList(QDir::Dirs | QDir::NoDotAndDotDot)) {
        QString sourceSubDirPath = sourceDir.filePath(subDir);
        QString destinationSubDirPath = destinationDir.filePath(subDir);
        if (!copyFolder(sourceSubDirPath, destinationSubDirPath)) {
            qWarning() << "Failed to copy subdirectory:" << sourceSubDirPath;
            return false;
        }
    }

    return true;
}

int isInternetEnabled() {
    QNetworkAccessManager manager;
    QNetworkRequest request(QUrl("http://www.google.com"));
    QEventLoop loop;

    QObject::connect(&manager, &QNetworkAccessManager::finished, &loop, &QEventLoop::quit);
    QNetworkReply* reply = manager.get(request);
    loop.exec();

    if (reply->error() == QNetworkReply::NoError) {
        reply->deleteLater();
        return 1; // Internet is available
    } else {
        reply->deleteLater();
        return 0; // No internet connection
    }
}

int compareVersions(const QString &version1, const QString &version2) {
    QStringList v1Parts = version1.split('.');
    QStringList v2Parts = version2.split('.');

    for (int i = 0; i < qMax(v1Parts.size(), v2Parts.size()); ++i) {
        int v1 = (i < v1Parts.size()) ? v1Parts[i].toInt() : 0;
        int v2 = (i < v2Parts.size()) ? v2Parts[i].toInt() : 0;

        if (v1 < v2) return -1;
        if (v1 > v2) return 1;
    }
    return 0;
}

void unZipExiftoolDownload(const QString &zipFilePath, const QString &outputDir , const QString exif_path)
{
    QString program = "powershell";
    QStringList arguments;
    arguments << "-Command" << QString("Expand-Archive -Path '%1' -DestinationPath '%2' -Force")
                                   .arg(zipFilePath).arg(outputDir);

    QProcess unzipProcess;
    unzipProcess.start(program, arguments);

    if (!unzipProcess.waitForFinished()) {
        qWarning() << "Error unzipping:" << unzipProcess.errorString();
        return;
    }

    QString output = unzipProcess.readAllStandardOutput();
    QString errorOutput = unzipProcess.readAllStandardError();
    if (!errorOutput.isEmpty()) {
        qWarning() << "Unzip Error:" << errorOutput;
    } else {
        qDebug() << "Unzipped successfully to" << outputDir;
    }

    QFile::copy(QDir::currentPath()+"/exiftool-"+exif_path+"_64/exiftool(-k).exe",QDir::currentPath()+"/exiftool.exe");
    qDebug()<<QDir::currentPath()+"/exiftool-"+exif_path+"_64/exiftool(-k).exe";
    QDir dir(QDir::currentPath()+"/exiftool-"+exif_path+"_64");
    copyFolder(QDir::currentPath()+"/exiftool-"+exif_path+"_64/exiftool_files",QDir::currentPath()+"/exiftool_files");
    dir.removeRecursively();
    QFile::remove("exiftool.zip");

}

bool MainWindow::copyLogsToDirectory(const QString &destinationDir) {

    QDir destDir(destinationDir);
    QString destInputPath = destDir.filePath("input.log");
    if (!QFile::copy(this->AppPath+"/input.log", destInputPath)) {
        qWarning() << "Failed to copy input.log to" << destInputPath;
        return false;
    } else {
        qDebug() << "Copied input.log to" << destInputPath;
    }

    QString destOutputPath = destDir.filePath("output.log");
    if (!QFile::copy(this->AppPath+"/output.log", destOutputPath)) {
        qWarning() << "Failed to copy output.log to" << destOutputPath;
        return false;
    } else {
        qDebug() << "Copied output.log to" << destOutputPath;
    }

    return true;
}

void MainWindow::selectFolder() {
    QString folderName = QFileDialog::getExistingDirectory(this, tr("Select Folder"), QString(),
                                                           QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks);

    if (!folderName.isEmpty()) {
        QMessageBox::information(this, tr("Selected Folder"), folderName);
    } else {
        QMessageBox::warning(this, tr("No Folder Selected"), tr("No folder was selected."));
    }
    ui->label->setText(folderName);
    this->isFile = 0;
    this->isFolder = 1;
}

void MainWindow::selectFile() {
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"), QString(),
                                                    tr("All Files (*)"));

    if (!fileName.isEmpty()) {
        QMessageBox::information(this, tr("Selected File"), fileName);
    } else {
        QMessageBox::warning(this, tr("No File Selected"), tr("No file was selected."));
    }
    ui->label->setText(fileName);
    this->isFile = 1;
    this->isFolder = 0;
}

void MainWindow::processFile(const QString &filename){
    QFile inputLog("input.log");
    QFile outputLog("output.log");

    if (!inputLog.open(QIODevice::WriteOnly | QIODevice::Text) ||
        !outputLog.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qWarning() << "Failed to open log files.";
        return;
    }
    QString filePath = filename;
    QTextStream inputStream(&inputLog);
    QTextStream outputStream(&outputLog);
    // Get and log input EXIF data
    QProcess inputProcess;
    inputProcess.start(this->exiftoolPath, QStringList() << filePath);
    inputProcess.waitForFinished();
    QString inputOutput = inputProcess.readAllStandardOutput().trimmed();
    inputStream << "\n" << inputOutput << "\n";

    // Clear all EXIF data
    QProcess clearProcess;
    clearProcess.start(this->exiftoolPath, QStringList() << "-all=" << filePath);
    clearProcess.waitForFinished();
    clearProcess.readAllStandardOutput(); // Ignore output

    // Get and log output EXIF data
    QProcess outputProcess;
    outputProcess.start(this->exiftoolPath, QStringList() << filePath);
    outputProcess.waitForFinished();
    QString outputOutput = outputProcess.readAllStandardOutput().trimmed();

    outputStream << "\n" << outputOutput << "\n";
    QMessageBox msgBox;
    if(inputLog.size() < outputLog.size()){
        msgBox.setText("Metadata Removal done successfully!");
    }
    else{
        msgBox.setText("Metadata Removal done!");
    }
    msgBox.exec();
    QFileInfo fileInfo(filePath);
    copyLogsToDirectory(fileInfo.absolutePath());

}

/*
void MainWindow::processFiles(const QString &directory) {

    DownloadProgress *obj = new DownloadProgress();
    int progress = 10;
    obj->displayProgress(progress,"Processing Folder");
    obj->show();
    QDir dir(directory);
    QStringList files = dir.entryList(QDir::Files | QDir::NoDotAndDotDot);
    int fileCount = files.size();
    if (files.isEmpty()) {
        qWarning() << "No files found in the directory.";
        return;
    } else {
        int incrementPerFile = 90 / fileCount;
        QFile inputLog("input.log");
        QFile outputLog("output.log");

        if (!inputLog.open(QIODevice::WriteOnly | QIODevice::Text) ||
            !outputLog.open(QIODevice::WriteOnly | QIODevice::Text)) {
            qWarning() << "Failed to open log files.";
            return;
        }

        QTextStream inputStream(&inputLog);
        QTextStream outputStream(&outputLog);

        for (const QString &file : files) {
            QString filePath = dir.filePath(file);

            // Get and log input EXIF data
            QProcess inputProcess;
            inputProcess.start(this->exiftoolPath, QStringList() << filePath);
            inputProcess.waitForFinished();
            QString inputOutput = inputProcess.readAllStandardOutput().trimmed();

            inputStream << "\n" << inputOutput << "\n";

            // Clear all EXIF data
            QProcess clearProcess;
            clearProcess.start(this->exiftoolPath, QStringList() << "-all=" << filePath);
            clearProcess.waitForFinished();
            clearProcess.readAllStandardOutput(); // Ignore output


            // Get and log output EXIF data
            QProcess outputProcess;
            outputProcess.start(this->exiftoolPath, QStringList() << filePath);
            outputProcess.waitForFinished();
            QString outputOutput = outputProcess.readAllStandardOutput().trimmed();
            progress+=incrementPerFile;
            obj->displayProgress(progress,filePath);
            outputStream << "\n" << outputOutput << "\n";
        }

        inputLog.close();
        outputLog.close();
        QMessageBox msgBox;
        if(inputLog.size() < outputLog.size()){
            msgBox.setText("Metadata Removal done successfully!");
        }
        else{
            msgBox.setText("Metadata Removal done!");
        }
        msgBox.exec();
        copyLogsToDirectory(directory);
    }

}*/

void MainWindow::processFiles(const QString &directory) {
    // Create progress dialog with parent
    DownloadProgress *progressDialog = new DownloadProgress(this);
    progressDialog->show();

    // Use QtConcurrent for background processing
    QFutureWatcher<void> *watcher = new QFutureWatcher<void>(this);

    QFuture<void> future = QtConcurrent::run([this, directory, progressDialog]() {
        QDir dir(directory);
        QStringList files = dir.entryList(QDir::Files | QDir::NoDotAndDotDot);

        // Early exit if no files
        if (files.isEmpty()) {
            QMetaObject::invokeMethod(progressDialog, [progressDialog]() {
                QMessageBox::warning(nullptr, "Error", "No files found in directory");
                progressDialog->close();
            }, Qt::QueuedConnection);
            return;
        }

        int fileCount = files.size();
        int incrementPerFile = 80 / fileCount;
        int currentProgress = 10;

        // Prepare log files
        QFile inputLog("input.log");
        QFile outputLog("output.log");

        if (!inputLog.open(QIODevice::WriteOnly | QIODevice::Text) ||
            !outputLog.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QMetaObject::invokeMethod(progressDialog, [progressDialog]() {
                QMessageBox::critical(nullptr, "Error", "Failed to open log files");
                progressDialog->close();
            }, Qt::QueuedConnection);
            return;
        }

        QTextStream inputStream(&inputLog);
        QTextStream outputStream(&outputLog);

        // Process each file
        for (const QString &file : files) {
            QString filePath = dir.filePath(file);

            // Update progress
            currentProgress += incrementPerFile;
            QMetaObject::invokeMethod(progressDialog,
                                      [progressDialog, currentProgress, filePath]() {
                                          progressDialog->displayProgress(currentProgress, filePath.split("/").last());
                                      },
                                      Qt::QueuedConnection
                                      );

            // Process EXIF data
            QProcess inputProcess, clearProcess, outputProcess;

            // Get input EXIF data
            inputProcess.start(this->exiftoolPath, QStringList() << filePath);
            inputProcess.waitForFinished();
            QString inputOutput = inputProcess.readAllStandardOutput().trimmed();
            inputStream << "\n" << inputOutput << "\n";

            // Clear EXIF data
            clearProcess.start(this->exiftoolPath, QStringList() << "-all=" << filePath);
            clearProcess.waitForFinished();

            // Get output EXIF data
            outputProcess.start(this->exiftoolPath, QStringList() << filePath);
            outputProcess.waitForFinished();
            QString outputOutput = outputProcess.readAllStandardOutput().trimmed();
            outputStream << "\n" << outputOutput << "\n";
        }

        // Close log files
        inputLog.close();
        outputLog.close();

        // Final processing and notification
        QMetaObject::invokeMethod(this, [this, directory, progressDialog]() {
            QMessageBox msgBox;
            msgBox.setText("Metadata Removal Completed!");
            msgBox.exec();

            // Copy logs
            copyLogsToDirectory(directory);

            // Close progress dialog
            progressDialog->displayProgress(90, "Processing Complete");
            progressDialog->close();
        }, Qt::QueuedConnection);
    });

    // Connect watcher to handle completion
    connect(watcher, &QFutureWatcher<void>::finished, this, [watcher]() {
        watcher->deleteLater();
    });

    watcher->setFuture(future);
}


QString MainWindow::getExifToolVersion() {
    QProcess process;
    process.start(this->exiftoolPath, QStringList() << "-ver");

    if (!process.waitForFinished()) {
        qWarning() << "Failed to execute exiftool.";
        return QString();
    }

    QString output = process.readAllStandardOutput().trimmed();
    qWarning() << "output is ::"<<output;
    if (output.isEmpty()) {
        qWarning() << "No output received from exiftool.";
        return QString();
    }

    return output;
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow) ,  backgroundWidget(new BackgroundWidget(this))

{
    ui->setupUi(this);
    ui->gridLayout->addWidget(backgroundWidget);
    this->exiftoolPath = QDir::currentPath()+"/exiftool.exe",
        connect(ui->actionAbout, &QAction::triggered, this, &MainWindow::show_about);
    connect(ui->actionreportissues, &QAction::triggered, this, &MainWindow::report_issues);
    connect(ui->actionCheck_for_Updates, &QAction::triggered, this, &MainWindow::download_exiftool);

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_selectFileButton_clicked()
{
    this->selectFile();
}

void MainWindow::show_about()
{
    QMessageBox::about(this, "About Metadata Remover",
                       "Metadata Remover  v2.0\n\n"
                       "A simple Metadata Removal Tool for removing metadata from images. Developed by M. Anish <aneesh25861@gmail.com>"

                       "\n\n===Credits===\n"
                       "\nIcons from Metadata Cleaner Project of Romain Vigier"
                       "\nExiftool developers"
                       );
}

void MainWindow::report_issues()
{
    QUrl url("https://github.com/Anish-M-code/Metadata-Remover");
    QDesktopServices::openUrl(url);
}

void MainWindow::download_exiftool()
{
    ContentReader *reader = new ContentReader(this);
    DownloadProgress *obj = new DownloadProgress(this);
    obj->show();
    obj->displayProgress(5," Attempting to connect Exiftool servers...");
    QString exiftool_url = "https://exiftool.org/exiftool-";

    QTimer *timeoutTimer = new QTimer(this);
    timeoutTimer->setSingleShot(true);
    timeoutTimer->setInterval(10000); // 10 seconds timeout

    QObject::connect(timeoutTimer, &QTimer::timeout, this, [this, reader, obj, timeoutTimer]() {
        qWarning() << "Connection timeout";
        obj->displayProgress(0, "Connection timeout. Unable to fetch version.");
        reader->deleteLater();
        timeoutTimer->deleteLater();
    });

    // Fetch the latest version from the server
    QObject::connect(reader, &ContentReader::contentReceived, this, [this, reader, obj ,timeoutTimer, exiftool_url](const QString &content) mutable {
        QString latest_exiftool_version = content.trimmed();
        QString full_exiftool_url = exiftool_url + latest_exiftool_version + "_64.zip";
        timeoutTimer->stop();
        obj->displayProgress(10,"checking new versions...");
        // Compare versions only if a valid version was retrieved
        QString currentVersion = getExifToolVersion();
        if (!latest_exiftool_version.isEmpty() && compareVersions(currentVersion, latest_exiftool_version) < 0) {
            // Download the file if the current version is lower than the latest version
            qDebug() << "Starting download...";
            obj->displayProgress(15,"starting download...");
            QObject::connect(reader, &ContentReader::downloadFinished, this, [this,obj, latest_exiftool_version, reader](bool success) {
                if (success) {
                    QTimer::singleShot(0, this, [this,obj, latest_exiftool_version]() {
                        obj->displayProgress(20,"Extracting Exiftool...");
                        unZipExiftoolDownload("exiftool.zip", ".", latest_exiftool_version);
                        obj->displayProgress(100,"Downloaded successfully");
                    });
                } else {
                    qWarning() << "Failed to download the file.";
                    obj->displayProgress(0,"Unable to download Exiftool...");
                }
                reader->deleteLater();
            });

            reader->downloadFile(QUrl(full_exiftool_url), "exiftool.zip");
        } else {
            qDebug() << "Current version is up to date or invalid latest version.";
            obj->displayProgress(100,"Current version is up to date!");
            reader->deleteLater();
        }

    });

    timeoutTimer->start();

    // Fetch the latest version text
    reader->fetchContent(QUrl("https://exiftool.org/ver.txt"));
}

void MainWindow::on_cleanButton_clicked()
{

    if(this->isFile){
        processFile(ui->label->text());
    }
    else if(this->isFolder){
        processFiles(ui->label->text());
    }


}

void MainWindow::on_selectFolderButton_clicked()
{
    this->selectFolder();
}


