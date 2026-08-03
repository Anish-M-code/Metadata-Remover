#include "workerthread.h"
#include <QFile>
#include <QProcess>
#include <QTextStream>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QEventLoop>
#include <QUrl>

DownloadWorker::DownloadWorker(const QString &url, const QString &destPath, QObject *parent)
    : QObject(parent), m_url(url), m_destPath(destPath)
{
}

void DownloadWorker::process()
{
      emit statusUpdate("Attempting to connect Exiftool servers...");

    QNetworkAccessManager manager;
    QNetworkRequest request((QUrl(m_url)));

    QNetworkReply *reply = manager.get(request);
    QEventLoop loop;
    connect(reply, &QNetworkReply::finished, &loop, &QEventLoop::quit);

    connect(reply, &QNetworkReply::downloadProgress, this, [this](qint64 bytesReceived, qint64 bytesTotal) {
        if (bytesTotal > 0) {
            int percent = static_cast<int>((bytesReceived * 100) / bytesTotal);
            emit progress(percent);
        }
    });

    loop.exec();

    if (reply->error() == QNetworkReply::NoError) {
        QFile file(m_destPath);
        if (file.open(QIODevice::WriteOnly)) {
            file.write(reply->readAll());
            file.close();
            emit finished(true);
        } else {
            emit error("Failed to open local file for writing: " + m_destPath);
            emit finished(false);
        }
    } else {
        emit error("Download error: " + reply->errorString());
        emit finished(false);
    }
    reply->deleteLater();
}

RemovalWorker::RemovalWorker(const QStringList &files, const QString &exiftoolPath, QObject *parent)
    : QObject(parent), m_files(files), m_exiftoolPath(exiftoolPath)
{
}

void RemovalWorker::process()
{
      QFile inputLog("input.log");
    QFile outputLog("output.log");
    if (!inputLog.open(QIODevice::WriteOnly | QIODevice::Text) || 
              !outputLog.open(QIODevice::WriteOnly | QIODevice::Text)) {
        emit error("Failed to open log files.");
        emit finished();
        return;
    }

    QTextStream inputStream(&inputLog);
    QTextStream outputStream(&outputLog);

    int totalFiles = m_files.size();
    if (totalFiles == 0) {
        emit finished();
        return;
    }

    for (int i = 0; i < totalFiles; ++i) {
        QString filePath = m_files[i];

        emit statusUpdate(filePath.split("/").last());

        QProcess inputProcess;
        inputProcess.start(m_exiftoolPath, QStringList() << filePath);
        if (!inputProcess.waitForFinished()) {
            emit fileProcessed(filePath, false);
            continue;
        }
        QString inputOutput = inputProcess.readAllStandardOutput().trimmed();
        inputStream << "\n" << inputOutput << "\n";

        QProcess clearProcess;
        clearProcess.start(m_exiftoolPath, QStringList() << "-all=" << filePath);
        if (!clearProcess.waitForFinished()) {
            emit fileProcessed(filePath, false);
            continue;
        }

        QProcess outputProcess;
        outputProcess.start(m_exiftoolPath, QStringList() << filePath);
        if (!outputProcess.waitForFinished()) {
            emit fileProcessed(filePath, false);
            continue;
        }
        QString outputOutput = outputProcess.readAllStandardOutput().trimmed();
        outputStream << "\n" << outputOutput << "\n";

        emit fileProcessed(filePath, true);

        int percent = static_cast<int>(((i + 1) * 100) / totalFiles);
        emit progress(percent);
    }

    inputLog.close();
    outputLog.close();
    emit finished();
}
