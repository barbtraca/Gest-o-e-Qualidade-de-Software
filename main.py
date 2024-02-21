from src.ui import App

app = App()
app.protocol("WM_DELETE_WINDOW", app.stop_player)
app.mainloop()
