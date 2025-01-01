#ifndef DOWNLOADPROGRESS_H
#define DOWNLOADPROGRESS_H

#include <QDialog>

namespace Ui {
class DownloadProgress;
}

class DownloadProgress : public QDialog
{
    Q_OBJECT

public:
    explicit DownloadProgress(QWidget *parent = nullptr);
    ~DownloadProgress();
    void displayProgress(int value, QString msg);

private slots:
    void on_pushButton_clicked();

private:
    Ui::DownloadProgress *ui;
};

#endif // DOWNLOADPROGRESS_H
