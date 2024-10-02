#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QCoreApplication>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QFile>
#include <QDir>
#include <QDebug>
#include <QObject>
#include <QMainWindow>
#include <qlistwidget.h>
#include <QDialog>
#include "backgroundwidget.h"
#include "contentreader.h"
#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void setAppPath(){
        this->AppPath = QDir::currentPath();
    }
    QString getAppPath(){
        return this->AppPath;
    }
    QString getExifToolVersion();

signals:
    void updateListWidget(const QString &message);
    void processingFinished();

private slots:
    void on_selectFileButton_clicked();
    void show_about();
    void report_issues();
    void download_exiftool();
    void selectFile();
    void selectFolder();
    void processFile(const QString&);
    void processFiles(const QString&);
    void on_cleanButton_clicked();
    void on_selectFolderButton_clicked();
    bool copyLogsToDirectory(const QString &destinationDir);

private:
    Ui::MainWindow *ui;
    BackgroundWidget *backgroundWidget;
    QListWidget *listWidget;
    QString AppPath;
    QString exiftoolPath;
    int isFile = 0;
    int isFolder = 0;
};

#endif // MAINWINDOW_H
