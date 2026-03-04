if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.workout.main",
        host="0.0.0.0",
        port=7000,
        loop="uvloop",
        restart=True,
    )
