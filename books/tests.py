from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Book, BookReview, Author, BookAuthor
from .forms import BookReviewForm


class BookViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(
            title='Book 1',
            description='Description 1',
            isbn='1234567890',
            cover_picture=SimpleUploadedFile(name='default-cover.jpeg', content=b'', content_type='image/jpeg')
        )
        cls.book2 = Book.objects.create(
            title='Book 2',
            description='Description 2',
            isbn='0987654321',
            cover_picture=SimpleUploadedFile(name='default-cover.jpeg', content=b'', content_type='image/jpeg')
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('books:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/list.html')
        self.assertContains(response, 'Book 1')
        self.assertContains(response, 'Book 2')

    def test_book_list_view_with_search_query(self):
        response = self.client.get(reverse('books:list'), {'q': 'Book 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book 1')
        self.assertNotContains(response, 'Book 2')


class BookDetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title='Book 1',
            description='Description 1',
            isbn='1234567890',
            cover_picture=SimpleUploadedFile(name='default-cover.jpeg', content=b'', content_type='image/jpeg')
        )

    def test_book_detail_view(self):
        response = self.client.get(reverse('books:detail', kwargs={'id': self.book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/detail.html')
        self.assertContains(response, 'Book 1')


class AddReviewViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.book = Book.objects.create(
            title='Book 1',
            description='Description 1',
            isbn='1234567890',
            cover_picture=SimpleUploadedFile(name='default-cover.jpeg', content=b'', content_type='image/jpeg')
        )

    def test_add_review_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('books:add_review', kwargs={'id': self.book.id}), {
            'stars_given': 5,
            'comment': 'Great book!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookReview.objects.count(), 1)
        self.assertEqual(BookReview.objects.first().comment, 'Great book!')

    def test_add_review_view_invalid_data(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('books:add_review', kwargs={'id': self.book.id}), {
            'stars_given': 6,  # Invalid star rating
            'comment': '',
        })
        self.assertEqual(response.status_code, 200)  # Should return to the same page with errors
        self.assertEqual(BookReview.objects.count(), 0)  # No review should be created


class EditReviewViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.book = Book.objects.create(
            title='Book 1',
            description='Description 1',
            isbn='1234567890',
            cover_picture=SimpleUploadedFile(name='default-cover.jpeg', content=b'', content_type='image/jpeg')
        )
        cls.review = BookReview.objects.create(book=cls.book, user=cls.user, stars_given=5, comment='Great book!')

    def test_edit_review_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('books:edit_review', kwargs={'book_id': self.book.id, 'review_id': self.review.id}), {
                'stars_given': 4,
                'comment': 'Good book!',
            })
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stars_given, 4)
        self.assertEqual(self.review.comment, 'Good book!')

    def test_edit_review_view_invalid_data(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('books:edit_review', kwargs={'book_id': self.book.id, 'review_id': self.review.id}), {
                'stars_given': 6,  # Invalid star rating
                'comment': '',
            })
        self.assertEqual(response.status_code, 200)  # Should return to the same page with errors
        self.review.refresh_from_db()
        self.assertEqual(self.review.stars_given, 5)  # Data should remain unchanged
        self.assertEqual(self.review.comment, 'Great book!')


class DeleteReviewViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.book = Book.objects.create(
            title='Book 1',
            description='Description 1',
            isbn='1234567890',
            cover_picture=SimpleUploadedFile(name='default-cover.jpeg', content=b'', content_type='image/jpeg')
        )
        cls.review = BookReview.objects.create(book=cls.book, user=cls.user, stars_given=5, comment='Great book!')

    def test_delete_review_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('books:delete_review', kwargs={'book_id': self.book.id, 'review_id': self.review.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookReview.objects.count(), 0)
