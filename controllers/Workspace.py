import os


class Workspace:
    previews_name_template = 'version_{}'
    workspace_path = 'workspace/'

    @staticmethod
    def copy_image_to_workspace(image_path):
        extension = image_path.split('.')[-1]
        final_file_path = Workspace.workspace_path + Workspace.previews_name_template.format(0) + '.' + extension
        image_data = open(image_path, 'rb').read()
        open(final_file_path, 'wb').write(image_data)

        return final_file_path

    @staticmethod
    def save_preview(image, extension):
        last_version = Workspace.get_last_preview() + 1
        preview_path = Workspace.workspace_path + Workspace.previews_name_template.format(last_version) + '.' + extension
        image.save(preview_path)

        return preview_path

    @staticmethod
    def get_last_preview():
        last = 0

        for file in os.listdir(Workspace.workspace_path):
            version = file.replace('version_', '').split('.')[0]

            if int(version) > last:
                last = int(version)

        return last

    @staticmethod
    def clear_work_space():
        for file in os.listdir(Workspace.workspace_path):
            os.remove(Workspace.workspace_path + file)