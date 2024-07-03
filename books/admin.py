from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'isbn']


admin.site.register(Book, BookAdmin)
admin.site.register(Author, BookAdmin)
admin.site.register(BookAuthor, BookAdmin)
admin.site.register(BookReview, BookAdmin)
