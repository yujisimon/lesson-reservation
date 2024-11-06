from django.test import TestCase
from django.urls import reverse, resolve
from ..views import IndexView, CourseApplicatedView

class TestUrls(TestCase):

  """index ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_index_url(self):
    view = resolve('/')
    #print(view)
    self.assertEqual(view.func.view_class, IndexView)

  """CourseApplicatedViewページへのリダイレクトをテスト"""
  def test_CourseApplicated_url(self):
    view = resolve('/course_applicated')
    self.assertEqual(view.func.view_class, CourseApplicatedView)