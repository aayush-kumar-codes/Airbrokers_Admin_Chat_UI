# from django.contrib import admin
# from django.utils.html import format_html  
# from .models import PDFUpload

# class PDFUploadAdmin(admin.ModelAdmin):
#     list_display = ('input_pdf', 'processed_pdf', 'form_data_json', 'normalized_data_json', 'uploaded_at')
#     fields = ('input_pdf', 'processed_pdf', 'form_data_json', 'normalized_data_json', 'uploaded_at')
#     readonly_fields = ('processed_pdf', 'form_data_json', 'normalized_data_json', 'uploaded_at')

#     def form_data_json(self, obj):
#         if obj.form_data_json:
#             return format_html('<a href="/media/{}/" target="_blank">View Form Data JSON</a>', obj.form_data_json)
#         return 'No Form Data'
    
#     def normalized_data_json(self, obj):
#         if obj.normalized_data_json:
#             return format_html('<a href="/media/{}/" target="_blank">View Normalized Data JSON</a>', obj.normalized_data_json)
#         return 'No Normalized Data'

# admin.site.register(PDFUpload, PDFUploadAdmin)


from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import PDFUpload
import json
import os

class PDFUploadAdmin(admin.ModelAdmin):
    list_display = ('input_pdf', 'processed_pdf', 'form_data_json', 'normalized_data_json', 'uploaded_at')
    fields = ('input_pdf', 'processed_pdf', 'form_data_json', 'normalized_data_json', 'uploaded_at')
    readonly_fields = ('processed_pdf', 'form_data_json', 'normalized_data_json', 'uploaded_at')

    def form_data_json(self, obj):
        """Display form_data.json with a clickable link that opens the JSON editor."""
        if obj.form_data_json:
            json_data = self.get_json_data(obj.form_data_json)
            return self.render_json_editor(json_data, 'form_data_json', obj.form_data_json.url)
        return 'No Data'

    def normalized_data_json(self, obj):
        """Display normalized_form_data.json with a clickable link that opens the JSON editor."""
        if obj.normalized_data_json:
            json_data = self.get_json_data(obj.normalized_data_json)
            return self.render_json_editor(json_data, 'normalized_data_json', obj.normalized_data_json.url)
        return 'No Data'

    def get_json_data(self, json_file):
        """Helper to load the JSON data from the file."""
        try:
            with open(json_file.path, 'r') as f:
                return json.load(f)
        except Exception as e:
            return str(e)

    def render_json_editor(self, json_data, field_name, file_url):
        """Render a clickable link for JSON data that opens in a JSON editor."""
        json_data_str = json.dumps(json_data, indent=2)
        return mark_safe(f"""
            <a href="javascript:void(0);" onclick="openJsonEditor('{file_url}', '{field_name}')">
                Open {field_name}
            </a>
            <div id="json_editor_{field_name}" style="display:none;">
                <textarea id="{field_name}_json_data" style="width: 100%; height: 400px;">{json_data_str}</textarea>
                <button onclick="saveJsonData('{field_name}')">Save Changes</button>
            </div>
        """)

admin.site.register(PDFUpload, PDFUploadAdmin)
