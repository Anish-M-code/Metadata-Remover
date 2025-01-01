#ifndef CONTENTREADER_H
#define CONTENTREADER_H

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

class ContentReader : public QObject
{
    Q_OBJECT

public:
    explicit ContentReader(QObject *parent = nullptr) : QObject(parent)
    {
        networkManager = new QNetworkAccessManager(this);
        connect(networkManager, &QNetworkAccessManager::finished, this, &ContentReader::onFinished);
    }
    void fetchContent(const QUrl &url);
    void downloadFile(const QUrl &url, const QString &filePath);

private slots:
    void onReadyRead();
    void onFinished();
    void onDownloadReadyRead();
    void onDownloadFinished();

signals:
    void contentReceived(const QString &content);
    void downloadFinished(bool success);

private:
    QNetworkAccessManager *networkManager;
    QFile m_file;
    QString m_filePath;
};

#endif // CONTENTREADER_H
