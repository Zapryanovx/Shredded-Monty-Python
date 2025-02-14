from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment, Like, SavedPost
from .forms import PostForm, CommentForm


class PostModelTest(TestCase):
    """Tests for the Post model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_post(self):
        """Tests if a post is created correctly."""
        post = Post.objects.create(user=self.user, text="Test post")
        self.assertEqual(post.user.username, "testuser")
        self.assertEqual(post.text, "Test post")


class CommentModelTest(TestCase):
    """Tests for the Comment model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, text="Test post")

    def test_create_comment(self):
        """Tests if a comment is created correctly."""
        comment = Comment.objects.create(user=self.user, post=self.post, text="Test comment")
        self.assertEqual(comment.user.username, "testuser")
        self.assertEqual(comment.text, "Test comment")


class LikeModelTest(TestCase):
    """Tests for the Like model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, text="Test post")

    def test_like_post(self):
        """Tests if a like is created correctly."""
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user.username, "testuser")
        self.assertEqual(like.post.text, "Test post")


class SavedPostModelTest(TestCase):
    """Tests for the SavedPost model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, text="Test post")

    def test_save_post(self):
        """Tests if a post is saved correctly."""
        saved_post = SavedPost.objects.create(user=self.user, post=self.post)
        self.assertEqual(saved_post.user.username, "testuser")
        self.assertEqual(saved_post.post.text, "Test post")


class PostFormTest(TestCase):
    """Tests for the Post form."""

    def test_valid_form(self):
        """Tests if a valid post form is accepted."""
        form_data = {'text': "Test post"}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Tests if an empty post form is rejected."""
        form_data = {'text': ""}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    """Tests for the Comment form."""

    def test_valid_form(self):
        """Tests if a valid comment form is accepted."""
        form_data = {'text': "Test comment"}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Tests if an empty comment form is rejected."""
        form_data = {'text': ""}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    """Tests for all views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, text="Test post")

    def test_social_feed_view(self):
        """Tests if the social feed page loads correctly."""
        response = self.client.get(reverse('social_feed'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_valid(self):
        """Tests creating a post with valid data."""
        response = self.client.post(reverse('create_post'), {'text': "New test post"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(text="New test post").exists())

    def test_create_post_invalid(self):
        """Tests creating a post with invalid data (empty text)."""
        response = self.client.post(reverse('create_post'), {'text': ""})
        self.assertEqual(response.status_code, 302)

    def test_delete_post(self):
        """Tests deleting a post."""
        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_add_comment_valid(self):
        """Tests adding a valid comment."""
        response = self.client.post(reverse('add_comment', args=[self.post.id]), {'text': "Test comment"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, text="Test comment").exists())

    def test_add_comment_invalid(self):
        """Tests adding an empty comment."""
        response = self.client.post(reverse('add_comment', args=[self.post.id]), {'text': ""})
        self.assertEqual(response.status_code, 302)

    def test_delete_comment(self):
        """Tests deleting a comment."""
        comment = Comment.objects.create(user=self.user, post=self.post, text="Test comment")
        response = self.client.post(reverse('delete_comment', args=[comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_like_post(self):
        """Tests liking a post."""
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_unlike_post(self):
        """Tests unliking a post."""
        Like.objects.create(user=self.user, post=self.post)
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_save_post(self):
        """Tests saving a post."""
        response = self.client.post(reverse('save_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SavedPost.objects.filter(user=self.user, post=self.post).exists())

    def test_unsave_post(self):
        """Tests unsaving a post."""
        SavedPost.objects.create(user=self.user, post=self.post)
        response = self.client.post(reverse('save_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SavedPost.objects.filter(user=self.user, post=self.post).exists())
