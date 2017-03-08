#include "appconfig.h"
#include "experimentcontext.h"

#include <QBoxLayout>
#include <QDebug>
#include <QDialog>
#include <QDialogButtonBox>
#include <QRadioButton>

template<typename TItem>
void ListContainer<TItem>::setCurrentIndexOrDefault(int index)
{
    if (checkIndex(index))
        _currenIndex = index;
    else if (!_items.isEmpty())
        _currenIndex = 0;
    else _currenIndex = -1;
}

template<typename TItem>
bool ListContainer<TItem>::selectCurrentViaDialog()
{
    QDialog dlg;
    auto layout = new QVBoxLayout;
    QVector<QRadioButton*> flags;
    for (int i = 0; i < _items.size(); i++)
    {
        auto flag = new QRadioButton(_items.at(i).title());
        flag->setChecked(i == _currenIndex);
        layout->addWidget(flag);
        flags << flag;
    }
    auto buttons = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
    dlg.connect(buttons, SIGNAL(accepted()), &dlg, SLOT(accept()));
    dlg.connect(buttons, SIGNAL(rejected()), &dlg, SLOT(reject()));
    layout->addSpacing(12);
    layout->addWidget(buttons);
    dlg.setLayout(layout);
    bool res = dlg.exec() == QDialog::Accepted;
    if (res)
        for (int i = 0; i < flags.size(); i++)
            if (flags.at(i)->isChecked())
                setCurrentIndex(i);
    return res;
}

template class ListContainer<DnnModel>;
template class ListContainer<DnnEngine>;
template class ListContainer<ImagesDataset>;

//-----------------------------------------------------------------------------

void ExperimentContext::startExperiment()
{
    _isExperimentStarted = true;
    emit experimentStarted();
}

void ExperimentContext::stopExperiment()
{
    _isExperimentStarted = false;
    emit experimentStopping();
}

void ExperimentContext::loadFromConfig()
{
    _models.setCurrentIndexOrDefault(0);
    _engines.setCurrentIndexOrDefault(0);
    _images.setCurrentIndexOrDefault(0);
}

