#ifndef WORKERTHREAD_H
#define WORKERTHREAD_H

#include <QObject>
#include <QThread>
#include <QStringList>
#include <QString>

class DownloadWorker : public QObject
{
    Q_OBJECT
public:
    explicit DownloadWorker(const QString &url, const QString &destPath, QObject *parent = nullptr);

public slots:
    void process();

signals:
    void progress(int percent);
    void statusUpdate(const QString &msg);
    void finished(bool success);
    void error(const QString &msg);

private:
    QString m_url;
    QString m_destPath;
};

class RemovalWorker : public QObject
{
    Q_OBJECT
public:
    explicit RemovalWorker(const QStringList &files, const QString &exiftoolPath, QObject *parent = nullptr);

public slots:
    void process();

signals:
    void progress(int percent);
    void fileProcessed(const QString &filePath, bool success);
    void statusUpdate(const QString &msg);
    void finished();
    void error(const QString &msg);

private:
    QStringList m_files;
    QString     m_exiftoolPath;
};

#endif // WORKERTHREAD_H
