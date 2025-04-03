def save_graph_as_png(app, file_path):
    """
    Saves the LangGraph workflow as a PNG file.
    Args:
        app: Compiled LangGraph workflow
        file_path (str): Path to save the PNG file
    """
    try:
        app.get_graph().draw_png(file_path)
        print(f"Agent graph saved as {file_path}")
    except Exception as e:
        print(f"Error saving agent graph: {e}")