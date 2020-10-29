import inspect
import logging
import os
import win32serviceutil
from notebook.notebookapp import NotebookApp, JupyterApp

# 作为服务运行时的工作目录是system32，这里改为文件所在目录
current_file = r'C:\Users\13164\Documents\Unicdata_Chen\some_demo'
os.chdir(os.path.dirname(current_file))


class NotebookService(win32serviceutil.ServiceFramework):
    _svc_name_ = "JupyterNotebook"
    _svc_display_name_ = "Jupyter Notebook Service"
    _svc_description_ = "Jupyter的服务啦"

    def __init__(self, args):
        super().__init__(args)
        self.app = NotebookApp()

    def _init_notebook(self):
        JupyterApp.initialize(self.app)
        self.app.init_configurables()
        self.app.init_components()
        self.app.init_webapp()
        self.app.init_terminals()
        self.app.init_server_extensions()
        self.app.init_mime_overrides()
        self.app.init_shutdown_no_activity()

    def SvcDoRun(self):
        self.app.config_dir = "config"  # 设置配置文件目录
        self._init_notebook()
        logging.getLogger("NotebookApp").addHandler(logging.FileHandler("notebook.log"))
        self.app.start()

    def SvcStop(self):
        self.app.stop()

    def SvcShutdown(self):
        self.SvcStop()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(NotebookService)
