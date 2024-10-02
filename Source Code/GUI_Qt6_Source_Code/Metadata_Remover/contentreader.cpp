#include "contentreader.h"

void ContentReader::fetchContent(const QUrl &url)
{
    QNetworkRequest request(url);
    QNetworkReply *reply = networkManager->get(request);

    connect(reply, &QNetworkReply::readyRead, this, &ContentReader::onReadyRead);
    connect(reply, &QNetworkReply::finished, this, &ContentReader::onFinished);
}
void ContentReader::downloadFile(const QUrl &url, const QString &filePath)
{
    QNetworkRequest request(url);
    QNetworkReply *reply = networkManager->get(request);

    connect(reply, &QNetworkReply::readyRead, this, &ContentReader::onDownloadReadyRead);
    connect(reply, &QNetworkReply::finished, this, &ContentReader::onDownloadFinished);

    m_filePath = filePath;
}

void ContentReader::onReadyRead()
{
    QNetworkReply *reply = qobject_cast<QNetworkReply*>(sender());
    if (reply)
    {
        QByteArray data = reply->readAll();
        qDebug() << "Content received:" << data;
        emit contentReceived(QString::fromUtf8(data));
    }
}

void ContentReader::onFinished()
{
    QNetworkReply *reply = qobject_cast<QNetworkReply*>(sender());
    if (reply)
    {
        if (reply->error() != QNetworkReply::NoError)
        {
            qWarning() << "Request failed:" << reply->errorString();
        }
        else
        {
            qDebug() << "Request completed successfully.";
        }
        reply->deleteLater();
    }
}
void ContentReader::onDownloadReadyRead()
{
    QNetworkReply *reply = qobject_cast<QNetworkReply*>(sender());
    if (reply)
    {

        if (!m_file.isOpen())
        {
            m_file.setFileName(m_filePath);
            if (!m_file.open(QIODevice::WriteOnly))
            {
                qWarning() << "Failed to open file for writing:" << m_filePath;
                return;
            }
        }
        m_file.write(reply->readAll());
    }
}

void ContentReader::onDownloadFinished()
{
    QNetworkReply *reply = qobject_cast<QNetworkReply*>(sender());
    if (reply)
    {
        if (reply->error() != QNetworkReply::NoError)
        {
            qWarning() << "Request failed:" << reply->errorString();
            emit downloadFinished(false);
        }
        else
        {
            qDebug() << "Download completed successfully. File saved to:" << m_filePath;
            emit downloadFinished(true);
        }
        m_file.close();
        reply->deleteLater();
    }
}
