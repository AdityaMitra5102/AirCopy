from pywinauto import *
import win32com.client
def get_selected_files():
    try:
        shell=win32com.client.Dispatch("Shell.Application")
        folder_view=None
        filelist=[]
        for window in shell.Windows():
            if 'Explorer' in window.Name:
                folder_view=window
                break
        if folder_view is not None:
            selected_items=folder_view.Document.SelectedItems()
            for item in selected_items:
                filelist.append(item.Path)
            

        folder_view=shell.Windows().Item()
        if folder_view is not None:
            selected_items=folder_view.Document.SelectedItems()
            for item in selected_items:
                filelist.append(item.Path)
            
        
        return filelist
    except:
        return []

