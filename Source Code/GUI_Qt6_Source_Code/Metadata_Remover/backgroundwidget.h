#ifndef BACKGROUNDWIDGET_H
#define BACKGROUNDWIDGET_H

#include<QObject>
#include<QPixmap>
#include<QPaintEvent>
#include<QPainter>
#include<QWidget>

class BackgroundWidget : public QWidget {
    Q_OBJECT

public:
    BackgroundWidget(QWidget *parent = nullptr)
        : QWidget(parent), backgroundImage("icon.svg") {
        resize(100, 200);
    }

protected:
    void paintEvent(QPaintEvent *event) override {
        QPainter painter(this);
        painter.drawPixmap(rect(), backgroundImage);
    }

private:
    QPixmap backgroundImage;
};
#endif // BACKGROUNDWIDGET_H
