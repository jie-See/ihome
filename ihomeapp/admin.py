from django.contrib import admin

# Register your models here.
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('fitst_name', 'last_name', 'email')  # 展示
#     search_fields = ('fitst_name', 'last_name')  # 设置搜索
#
#
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publisher', 'publication_date')
#     list_filter = ('publication_date',)  # 筛选
#     date_hierarchy = 'publication_date'  # 增加导航栏
#     ordering = ('-publication_date',)  # 排序
#     # fields = ('authors', 'title', 'publisher')  # 设置编辑表单的顺序，若没有的字段，则在后台不能编辑
#     # filter_horizontal = ('authors',)  # 一个多选的过滤器
#     filter_vertical = ('authors',)  # 一个多选的过滤器,与上面一个样式不同
#     raw_id_fields = ('publisher',)  # 将选择器变成可搜索的选择器
#
# admin.site.register(Book, BookAdmin)