from django.db import models


class FileField(models.FileField):
    def save_form_data(self, instance, data):
        file = getattr(instance, self.attname)
        if file != data:
            try: os.remove(file.path)
            except: pass
        super(FileField, self).save_form_data(instance, data)