import tkinter as tk
from tkinter import messagebox,simpledialog
import json
import os
import datetime
class TaskManager:
    def __init__(self,root):
        self.root=root
        self.root.title("Менеджер задач")
        self.task_list=[]
        self.current_task=None
        self.loadtasks()
        self.frame=tk.Frame(root)
        self.frame.pack(padx=10,pady=10)
        self.task_label=tk.Label(self.frame,text="Описание задачи:")
        self.task_label.grid(row=0,column=0,sticky="w")
        self.task_entry=tk.Entry(self.frame,width=50)
        self.task_entry.grid(row=0,column=1,padx=5)
        self.priority_label=tk.Label(self.frame,text="Приоритет:")
        self.priority_label.grid(row=1,column=0,sticky="w")
        self.priority_var=tk.StringVar(value="Обычный")
        self.priority_menu=tk.OptionMenu(self.frame,self.priority_var,"Обычный","Высокий","Низкий")
        self.priority_menu.grid(row=1,column=1,padx=5)
        self.due_date_label=tk.Label(self.frame,text="Дата выполнения:")
        self.due_date_label.grid(row=2,column=0,sticky="w")
        self.due_date_entry=tk.Entry(self.frame,width=50)
        self.due_date_entry.grid(row=2,column=1,padx=5)
        self.add_button=tk.Button(self.frame,text="Добавить задачу",command=self.addtask)
        self.add_button.grid(row=3,column=0,columnspan=2,pady=5)
        self.task_listbox=tk.Listbox(self.frame,width=60,height=15)
        self.task_listbox.grid(row=4,column=0,columnspan=2,pady=5)
        self.task_listbox.bind('<<ListboxSelect>>',self.selecttask)
        self.delete_button=tk.Button(self.frame,text="Удалить задачу",command=self.deletetask)
        self.delete_button.grid(row=5,column=0,pady=5)
        self.update_button=tk.Button(self.frame,text="Изменить задачу",command=self.updatetask)
        self.update_button.grid(row=5,column=1,pady=5)
        self.complete_button=tk.Button(self.frame,text="Отметить как выполненную",command=self.markcompleted)
        self.complete_button.grid(row=6,column=0,pady=5)
        self.sort_button=tk.Button(self.frame,text="Сортировать по дате",command=self.sortbydate)
        self.sort_button.grid(row=6,column=1,pady=5)
        self.export_button=tk.Button(self.frame,text="Экспорт в CSV",command=self.exporttocsv)
        self.export_button.grid(row=7,column=0,pady=5)
        self.import_button=tk.Button(self.frame,text="Импорт из CSV",command=self.importfromcsv)
        self.import_button.grid(row=7,column=1,pady=5)
        self.clear_button=tk.Button(self.frame,text="Очистить все задачи",command=self.clearalltasks)
        self.clear_button.grid(row=8,column=0,columnspan=2,pady=5)
        self.task_count_label=tk.Label(self.frame,text=f"Количество задач: {len(self.task_list)}")
        self.task_count_label.grid(row=9,column=0,columnspan=2)
        self.filter_label=tk.Label(self.frame,text="Фильтровать по статусу:")
        self.filter_label.grid(row=10,column=0,sticky="w")
        self.filter_var=tk.StringVar(value="Все")
        self.filter_menu=tk.OptionMenu(self.frame,self.filter_var,"Все","Выполненные","Не выполненные")
        self.filter_menu.grid(row=10,column=1,padx=5)
        self.filter_var.trace_add("write",self.filtertasks)
    def addtask(self):
        task_description=self.task_entry.get().strip()
        priority=self.priority_var.get()
        due_date=self.due_date_entry.get().strip()
        if task_description=="":
            messagebox.showwarning("Внимание","Пожалуйста,введите описание задачи.")
            return
        try:
            due_date_obj=datetime.datetime.strptime(due_date,"%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Ошибка","Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.")
            return
        task={
            'description': task_description,
            'priority': priority,
            'due_date': due_date_obj,
            'completed': False
        }
        self.task_list.append(task)
        self.updatetasklist()
        self.clearinputs()
        self.savetasks()
    def selecttask(self,event):
        try:
            index=self.task_listbox.curselection()[0]
            self.current_task=self.task_list[index]
            self.task_entry.delete(0,tk.END)
            self.task_entry.insert(tk.END,self.current_task['description'])
            self.priority_var.set(self.current_task['priority'])
            self.due_date_entry.delete(0,tk.END)
            self.due_date_entry.insert(tk.END,self.current_task['due_date'].strftime("%Y-%m-%d"))
        except IndexError:
            pass
    def updatetask(self):
        if self.current_task is not None:
            task_description=self.task_entry.get().strip()
            priority=self.priority_var.get()
            due_date=self.due_date_entry.get().strip()
            if task_description=="":
                messagebox.showwarning("Внимание","Пожалуйста,введите описание задачи.")
                return
            try:
                due_date_obj=datetime.datetime.strptime(due_date,"%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Ошибка","Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.")
                return
            self.current_task['description']=task_description
            self.current_task['priority']=priority
            self.current_task['due_date']=due_date_obj
            self.updatetasklist()
            self.savetasks()
    def deletetask(self):
        if self.current_task is not None:
            self.task_list.remove(self.current_task)
            self.updatetasklist()
            self.clearinputs()
            self.savetasks()
    def markcompleted(self):
        if self.current_task is not None:
            self.current_task['completed']=True
            self.updatetasklist()
            self.savetasks()
    def sortbydate(self):
        self.task_list.sort(key=lambda x: x['due_date'])
        self.updatetasklist()
    def exporttocsv(self):
        try:
            with open("tasks.csv","w") as f:
                f.write("Описание,Приоритет,Дата выполнения,Выполнена\n")
                for task in self.task_list:
                    f.write(
                        f"{task['description']},{task['priority']},{task['due_date'].strftime('%Y-%m-%d')},{task['completed']}\n")
            messagebox.showinfo("Успех","Задачи успешно экспортированы в tasks.csv.")
        except Exception as e:
            messagebox.showerror("Ошибка",f"Ошибка при экспорте данных: {str(e)}")
    def importfromcsv(self):
        try:
            with open("tasks.csv","r") as f:
                lines=f.readlines()[1:]
                for line in lines:
                    description,priority,due_date,completed=line.strip().split(',')
                    due_date_obj=datetime.datetime.strptime(due_date,"%Y-%m-%d")
                    completed=completed.lower()=="true"
                    task={
                        'description': description,
                        'priority': priority,
                        'due_date': due_date_obj,
                        'completed': completed
                    }
                    self.task_list.append(task)
            self.updatetasklist()
            messagebox.showinfo("Успех","Задачи успешно импортированы из tasks.csv.")
        except Exception as e:
            messagebox.showerror("Ошибка",f"Ошибка при импорте данных: {str(e)}")
    def clearalltasks(self):
        answer=messagebox.askyesno("Очистка","Вы уверены,что хотите удалить все задачи?")
        if answer:
            self.task_list.clear()
            self.updatetasklist()
            self.savetasks()
    def updatetasklist(self):
        self.task_listbox.delete(0,tk.END)
        for task in self.task_list:
            status="Выполнена" if task['completed'] else "Не выполнена"
            task_text=f"{task['description']} | Приоритет: {task['priority']} | Дата: {task['due_date'].strftime('%Y-%m-%d')} | {status}"
            self.task_listbox.insert(tk.END,task_text)
        # Обновить информацию о количестве задач
        self.task_count_label.config(text=f"Количество задач: {len(self.task_list)}")
    def clearinputs(self):
        self.task_entry.delete(0,tk.END)
        self.due_date_entry.delete(0,tk.END)
        self.priority_var.set("Обычный")
        self.current_task=None
    def savetasks(self):
        try:
            with open("tasks.json","w") as f:
                json.dump(self.task_list,f,default=str,indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка",f"Не удалось сохранить задачи: {str(e)}")
    def loadtasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json","r") as f:
                    self.task_list=json.load(f)
                    for task in self.task_list:
                        task['due_date']=datetime.datetime.strptime(task['due_date'],"%Y-%m-%d")
                self.updatetasklist()
            except Exception as e:
                messagebox.showerror("Ошибка",f"Не удалось загрузить задачи: {str(e)}")
    def filtertasks(self,*args):
        filter_status=self.filter_var.get()
        if filter_status=="Все":
            filtered_tasks=self.task_list
        elif filter_status=="Выполненные":
            filtered_tasks=[task for task in self.task_list if task['completed']]
        elif filter_status=="Не выполненные":
            filtered_tasks=[task for task in self.task_list if not task['completed']]
        self.task_listbox.delete(0,tk.END)
        for task in filtered_tasks:
            status="Выполнена" if task['completed'] else "Не выполнена"
            task_text=f"{task['description']} | Приоритет: {task['priority']} | Дата: {task['due_date'].strftime('%Y-%m-%d')} | {status}"
            self.task_listbox.insert(tk.END,task_text)
if __name__=="__main__":
    root=tk.Tk()
    app=TaskManager(root)
    root.mainloop()