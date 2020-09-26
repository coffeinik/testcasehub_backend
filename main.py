from .casehub import create_app


if __name__ == "__main__":
    app = create_app("config.yaml")
    app.run(host="0.0.0.0", port=5000, debug=True)
