from fastai.text import *

class EarlyStopping(Callback):
    def __init__(self,learner,save_path):
        super().__init__()
        self.learner=learner
        self.save_path=save_path
    def on_train_begin(self):
        self.best_val_loss=100.0
    def on_epoch_end(self,metrics):
        val_loss = metrics[0]
        if val_loss < self.best_val_loss:
            self.best_val_loss=val_loss
            print (f'Saving model with loss: {val_loss}')
            torch.save(self.learner.state_dict(),'models/'+self.save_path)

