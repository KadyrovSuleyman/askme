from django import forms
from app.models import Question, Profile, Answer, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

  
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



# --------------------------------------------


class SettingsForm(forms.Form):

    def __init__(self, *args, **kwargs):
      user = None
      if len(args) == 3:
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.user = args[2]
      else:
        super(SettingsForm, self).__init__(*args, **kwargs)

    login = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)


    def clean(self):
      cleaned_data = super().clean()
      user_one = None
      user_two = None
      if cleaned_data.get('login'):
        user_one = User.objects.filter(username = cleaned_data.get('login'))
      if cleaned_data.get('email'):
        user_two = User.objects.filter(email = cleaned_data.get('email'))
      if user_one and (user_one.get().id != self.user.id):
        self.add_error('login', 'This login has already been registered!')
      else:
        if user_two and (user_two.get().id != self.user.id):
          self.add_error('email', 'This email has already been registered!')
      return cleaned_data

# --------------------------------------------

class AskForm(forms.ModelForm):
    tags = forms.CharField()
    class Meta:
        model = Question
        fields = ['title', 'text']
        labels = { 'title': "Header", 'text': "Text",}
       
 


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = { 'text': "", }
      


