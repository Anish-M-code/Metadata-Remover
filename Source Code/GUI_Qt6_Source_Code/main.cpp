#include "mainwindow.h"
#include <QApplication>
#include <QWidget>
#include <QPainter>
#include <QPixmap>
#include <QIcon>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    a.setWindowIcon(QIcon("icon-simple.svg"));
    MainWindow w;
    w.setAppPath();
    w.show();
    return a.exec();
}
