from django.test import TestCase, Client
from django.urls import reverse
from courses.models import CustomUser,Attendee,Course


class TestViews(TestCase):

    fixtures = ['courses']

    def setUp(self):
        user = CustomUser.objects.create_user(username = 'testuser', password = 'pass1234')
        self.client.force_login(user)


    def test_get_index(self):
        # GET メソッドでアクセスしてステータスコード200が返される
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_post_course_applicated(self):
        # データをPOSTしてステータスコード200が返される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        self.assertEqual(response.status_code, 200)
 

    def test_POST_success(self):
        # データをPOSTして「予約しました」が返される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        self.assertIn('予約しました', response.context['message'])
        
        
    def test_coursetype_updated(self):
        # データをPOSTして座席数が更新される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        course=Course.objects.get(coursetype="begin")
        self.assertEqual(course.mon, 1)


    def test_attended_updated(self):
        # データをPOSTして予約フラグが更新される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        user = CustomUser.objects.get(username='testuser')
        attendee =Attendee.objects.get(username=user)
        self.assertEqual(attendee.applicated, '100')

    def test_POST_bad_course(self):
        # 不適な講座申し込みを POSTして「受講資格はありません」が返される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "middle",
                "weekday": "mon",
                "action": "reg"})
        self.assertIn('受講資格はありません', response.context['message'])


    def test_post_tue(self):
        # 火曜申し込みをPOSTして「予約しました」が返される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "tue",
                "action": "reg"})
        self.assertIn('予約しました', response.context['message'])


    def test_POST_cancel(self):
        # cancelをPOSTして「中止しました」が返される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "middle",
                "weekday": "mon",
                "action": "can"})
        self.assertIn('中止しました', response.context['message'])


    def test_POST_additional(self):
        # 追加申し込みを　POSTして「申し込み済です」が返される
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})

        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})

        self.assertIn('申し込み済です', response.context['message'])


    def test_not_authenticated_user(self):
        # ログインしていないユーザーは投稿できず、ログインページにリダイレクトされる
        self.client.logout()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/")


class TestViewsFull(TestCase):

    fixtures = ['courses']

    def test_course_fill(self):
        # テストデータは席数が2，3人目の予約から「満席」になる

        user = CustomUser.objects.create_user(username = 'firstuser', password = 'pass1234')
        self.client.force_login(user)
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        self.assertIn('予約しました', response.context['message'])
        self.client.logout()

        user = CustomUser.objects.create_user(username = 'seconduser', password = 'pass1234')
        self.client.force_login(user)
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        self.assertIn('予約しました', response.context['message'])
        self.client.logout()

        user = CustomUser.objects.create_user(username = 'thirduser', password = 'pass1234')
        self.client.force_login(user)
        response = self.client.post(
            reverse("course_applicated"), {
                "course": "begin",
                "weekday": "mon",
                "action": "reg"})
        self.assertIn('満席です', response.context['message'])
        self.client.logout()
