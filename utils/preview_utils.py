# utils/preview_utils.py, refactored version

from .file_utils import create_directory, file_exists, list_files, join_paths

def save_model_response(model_name, response, uuid):
    """Save the model response in a Markdown file in the subdirectory labeled by the uuid."""
    # Create the subdirectory if it doesn't exist
    subdir_path = join_paths('responses', str(uuid))
    create_directory(subdir_path)  # Using create_directory from file_utils

    # Define the filename and path
    filename = f"{model_name}.md"
    file_path = join_paths(subdir_path, filename)

    # Write the response to the file
    with open(file_path, 'w') as f:
        f.write(response)

def list_responses(uuid):
    """List all response files in the subdirectory for the given uuid."""
    subdir_path = join_paths('responses', str(uuid))
    if file_exists(subdir_path):  # Using file_exists from file_utils
        return list_files(subdir_path)  # Using list_files from file_utils
    else:
        return []
