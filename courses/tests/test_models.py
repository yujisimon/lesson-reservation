from django.test import TestCase
from courses.models import Attendee, Course, CustomUser


class CustomUserModelTests(TestCase):

    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""  
        saved_customuser = CustomUser.objects.all()
        self.assertEqual(saved_customuser.count(), 0)


    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        customuser = CustomUser(username = 'testuser', password = 'pass1234')
        customuser.save()
        saved_customuser = CustomUser.objects.all()
        self.assertEqual(saved_customuser.count(), 1)


    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        customuser = CustomUser() # <-- 最初は customuser = CustomUser と誤入力してエラー
        username = 'testuser'
        password = 'pass1234'
        customuser.username = username
        customuser.password = password
        customuser.save()
        #customuser.save()https://qiita.com/yama04070319/items/1296ddfe27b6065df714
        #TypeError: AbstractBaseUser.save() missing 1 required positional argument: 'self'

        # https://qiita.com/yama04070319/items/1296ddfe27b6065df714
        # DjangoのViewでデータを追加する時　Error:save() missing 1 required positional argument: 'self'
        # FavoriteというDjangoモデルにuserとfavoriteのフィールドがあり、
        # そこにLikeしたユーザとその投稿の記事を紐づけたい時、初めはFav=Favoriteとしていた為、
        # エラーが生じていた。これをFav=Favorite()としてインスタンスを引き渡すと無事に解決出来た。
        # こちらの記事にも同じような事が記載されている。
        # https://stackoverflow.com/questions/46907511/typeerror-save-missing-1-required-positional-argument-self

        # エラーの原因は私のタイプミス


        saved_customuser = CustomUser.objects.all()
        actual_customuser = saved_customuser[0]

        self.assertEqual(actual_customuser.username, username)
        self.assertEqual(actual_customuser.password, password)


class AttendeeModelTests(TestCase):


    @classmethod
    def setUpTestData(cls):
        """クラスレベルでCustomUserインスタンスを1回だけ作成する"""
        cls.user = CustomUser.objects.create_user(username='testuser', password='pass1234')
        #cls.category = Category.objects.create(name="TestCategory")



    def test_created_onetoone(self):
        """1つレコードを作成すると、usernameがOneToOneFileldで対応するモデル間で一致している"""
        attendee = Attendee.objects.create(username = self.user)

        self.assertEqual(self.user.username , 'testuser')
        self.assertEqual((attendee.username.username) , 'testuser')
        #self.assertEqual((attendee.username) , 'testuser') のときは
        # AssertionError: <CustomUser: testuser> != 'testuser'  オブジェクトとstrの比較となりエラー

        all_attendee = Attendee.objects.all()
        self.assertEqual(all_attendee.count(), 1)

        all_attendee = Attendee.objects.all()
        self.assertEqual(all_attendee.count(), 1)


    def test_created_values(self):
        """1つレコードを作成すると、未入力Fileldにデフォールトがセットされる"""
        attendee = Attendee.objects.create(username=self.user)

        self.assertEqual(attendee.attended, '000')
        self.assertEqual(attendee.applicated, '000')



#
# class CourseTests(TestCase):
# 
#     fixtures = ['courses']
# 
#     def setUp(self):
#          fixtures = ['courses']
#          print('fixtures')
# 
#     def test_empty_values(self):
# 
#         all_ourse = Course.objects.all()
#         self.assertEqual(all_ourse.count(), 3)


class CourseModelTests(TestCase):

    fixtures = ['courses']

    #def setUp(self):
    #    fixtures = ['courses']  これは動かない
    #    print('fixtures')

    def test_initial_record_count(self):
        """初期設定されているレコード数"""
        all_course = Course.objects.all()
        self.assertEqual(all_course.count(), 3)

    def test_begin_default_values(self):
        """初期設定されているレコード内容"""
        course = Course.objects.get(coursetype="begin") 

        self.assertEqual(course.coursetype , 'begin')
        self.assertEqual(course.requisite , '000')
        self.assertEqual(course.mon , 2)
        self.assertEqual(course.tue , 2)
        self.assertEqual(course.wed , 2)

        #allcourses = Course.objects.all()
        #print('allcourses', allcourses.count())
        #for item in allcourses:
        #    print(item, item.coutype, item.coumask, item.mon, item.tue, item.wed )
        #print('allcourses', allcourses.count())

        #self.assertEqual(allcourses[0].coutype , 'begin')

        #all_ourse = Course.objects.all()
        #self.assertEqual(all_ourse.count(), 3)

    def test_middle_default_values(self):
        """初期設定されているレコード内容"""
        course = Course.objects.get(coursetype="middle")

        self.assertEqual(course.coursetype , 'middle')
        self.assertEqual(course.requisite , '100')
        self.assertEqual(course.mon , 2)
        self.assertEqual(course.tue , 2)
        self.assertEqual(course.wed , 2)


    def test_advance_default_values(self):
        """初期設定されているレコード内容"""
        course = Course.objects.get(coursetype="advance")

        self.assertEqual(course.coursetype , 'advance')
        self.assertEqual(course.requisite , '110')
        self.assertEqual(course.mon , 2)
        self.assertEqual(course.tue , 2)
        self.assertEqual(course.wed , 2)
