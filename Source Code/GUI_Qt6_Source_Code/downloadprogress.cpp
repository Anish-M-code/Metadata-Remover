#include "downloadprogress.h"
#include "ui_downloadprogress.h"

DownloadProgress::DownloadProgress(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::DownloadProgress)
{
    ui->setupUi(this);
    this->setWindowTitle("Metadata Remover");
}

DownloadProgress::~DownloadProgress()
{
    delete ui;
}

void DownloadProgress::displayProgress(int value, QString msg)
{
    ui->pushButton->setVisible(false);
    ui->label->setText(msg);
    ui->progressBar->setValue(value);
    if(value == 100 || value == 0){
        ui->pushButton->setVisible(true);
    }
}

void DownloadProgress::on_pushButton_clicked()
{
    this->hide();
}

