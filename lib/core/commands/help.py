import app.base.config_ui as config_ui

# Display help to make it easier for users to see what commands are available.
# Without this the user is confused about what commands are in storm.


def execute(args, context):
    config_ui.show_help()
    return context
