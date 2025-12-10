from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run slightly verbose for better debug info in console
    print("Starting Planner Pro Generator V3 (World Class)...")
    app.run(port=3000, debug=False)
