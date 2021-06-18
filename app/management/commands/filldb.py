from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, Vote, AnswerVote
from random import choice, randint, choices
from faker import Faker
from django.db.models import Count, Sum

f = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--db_size', type=str)


    def fill_users(self, cnt):
      users = []
      #Faker.seed(999999)
      for i in range(cnt):
        users.append(User(is_superuser=False, username=f.first_name() + str(f.random_int(min=1, max=9999)) + str(f.random_int(min=1, max=9999)) + f.word()))
      User.objects.bulk_create(users)


    def fill_profiles(self, cnt):
        profiles = []
        user_ids = list(User.objects.values_list('id', flat=True))
        #Faker.seed(999999)
        for i in range(cnt):
            profiles.append(Profile(
                user_id=user_ids[i],
                nickname=f.first_name() + ' ' + f.last_name(),
            ))
        Profile.objects.bulk_create(profiles)


    def fill_tags(self, cnt):
        tgs = []
        tag_names = []
        for i in range(cnt):
            tag_name = f.word()
            if (tag_name not in tag_names):
              tgs.append(Tag(name = tag_name))
              tag_names.append(tag_name)
        Tag.objects.bulk_create(tgs)


    def fill_questions(self, cnt):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))
        questions = []
        for i in range(cnt):
          questions.append(Question(
          user_id=choice(profile_ids), 
          text=' '.join(f.sentences(f.random_int(min=2, max=5))),
          title=f.sentence()[:-1] + '?',))
        Question.objects.bulk_create(questions)

        
  
    def fill_answers(self, cnt):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )

        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )

        correct = [True, False]
        answers = []
        for i in range(cnt):
          answers.append(Answer(
          user_id=choice(profile_ids),
          question_id=choice(question_ids),
          text='. '.join(f.sentences(f.random_int(min=1, max=5))),
          is_correct=choice(correct),
          rating = 0))
        Answer.objects.bulk_create(answers)


    def fill_question_votes(self, cnt):       
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        questions_ids = list(Question.objects.values_list('id', flat=True))
        question_votes = []
        for i in range(cnt):
          question_votes.append(Vote(
          user_id=choice(profile_ids), 
          question_id=choice(questions_ids), 
          value=choice([1, -1])))
        Vote.objects.bulk_create(question_votes)


    def fill_question_rating(self):
        questions = Question.objects.all().annotate(num_likes = Sum('vote__value'))
        for question in questions:
          if question.num_likes:
            question.rating = question.num_likes
          else:
            question.rating = 0
        Question.objects.bulk_update(questions, ['rating'])


    def fill_answer_votes(self, cnt):       
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        answer_ids = list(Answer.objects.values_list('id', flat=True))
        answer_votes = []
        for i in range(cnt):
          answer_votes.append(AnswerVote(
          user_id=choice(profile_ids), 
          answer_id=choice(answer_ids), 
          value=choice([1, -1])))
        AnswerVote.objects.bulk_create(answer_votes)


    def fill_answer_rating(self):
        answers = Answer.objects.all().annotate(num_likes = Sum('answervote__value'))
        for answer in answers:
          if answer.num_likes:
            answer.rating = answer.num_likes
          else:
            answer.rating = 0
        Answer.objects.bulk_update(answers, ['rating'])


    def fill_with_tags(self):
      t = Tag.objects.all()
      t_start = t[0].id
      t_end = t[len(t) - 1].id
      questions = Question.objects.all()
      for i in range(1, questions.count()):
        lst = list(range(t_start, t_end))
        questions[i].tags.set(choices(lst, k=3))
      



    def handle(self, *args, **options):
        small = 10
        medium = 1000
        large = 10000
        for a in options:
            if (options[a] == 'small'):
                self.fill_users(small)
                self.fill_profiles(small)
                self.fill_tags(small)
                self.fill_questions(small * 10)
                self.fill_answers(small * 100)
                self.fill_question_votes(small * 200)
                self.fill_answer_votes(small * 200)
                self.fill_question_rating()
                self.fill_answer_rating()
                self.fill_with_tags()

            if (options[a] == 'medium'):
                self.fill_users(medium)
                self.fill_profiles(medium)
                self.fill_tags(medium)
                self.fill_questions(medium * 10)
                self.fill_answers(medium * 100)
                self.fill_question_votes(medium * 200)
                self.fill_answer_votes(medium * 200)
                self.fill_question_rating()
                self.fill_answer_rating()
                self.fill_with_tags()

            if (options[a] == 'large'):
                self.fill_users(large)
                self.fill_profiles(large)
                self.fill_tags(large)
                self.fill_questions(large * 10)
                self.fill_answers(large * 100)
                self.fill_question_votes(large * 200)
                self.fill_answer_votes(large * 200)
                self.fill_question_rating()
                self.fill_answer_rating()
                self.fill_with_tags()
