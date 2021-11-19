import os
import json

class Workspace:
    previews_name_template = 'version_{}'
    workspace_path = 'workspace/'

    @staticmethod
    def copy_image_to_workspace(image_path):
        extension = image_path.split('.')[-1]
        final_file_path = Workspace.workspace_path + Workspace.previews_name_template.format(0) + '.' + extension
        changes_info_path = Workspace.workspace_path + Workspace.previews_name_template.format(0) + '.pxs'
        image_data = open(image_path, 'rb').read()

        open(final_file_path, 'wb').write(image_data)
        open(changes_info_path, 'w').write(str({}))

        return final_file_path

    @staticmethod
    def save_preview(image, extension, change):
        last_version = Workspace.get_last_preview() + 1
        preview_path = Workspace.workspace_path + Workspace.previews_name_template.format(last_version) + '.' + extension
        preview_changes_path = Workspace.workspace_path + Workspace.previews_name_template.format(last_version) + '.pxs'

        with open(preview_changes_path, 'w') as file:
            file.write(str(change).replace("'", '"'))

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

    @staticmethod
    def get_current_change():
        last_version = Workspace.get_last_preview()
        file_name = Workspace.workspace_path + Workspace.previews_name_template.format(last_version) + '.pxs'
        file_content = open(file_name, 'r').read()
        change = json.loads(file_content)

        return change

    @staticmethod
    def undo(extension):
        last_version = Workspace.get_last_preview()
        old_preview_path = Workspace.workspace_path + Workspace.previews_name_template.format(last_version) + '.' + extension
        old_preview_changes_path = Workspace.workspace_path + Workspace.previews_name_template.format(last_version) + '.pxs'

        os.remove(old_preview_path)
        os.remove(old_preview_changes_path)

        return Workspace.workspace_path + Workspace.previews_name_template.format(last_version-1) + '.' + extension
