from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView
import requests
import json

User = get_user_model()

class Indice(ListView):
    template_name = 'index.html'
    model = User


    def get_context_data(self, **kwargs):
        context = super(Indice, self).get_context_data(**kwargs)
        books = [
            "btc_mxn", "eth_mxn", "xrp_mxn", "ltc_mxn", "tusd_mxn", "mana_mxn", "gnt_mxn", "bat_mxn", "dai_mxn"
        ]
        result_dict = []
        for i in range(len(books)):
            url = 'https://api.bitso.com/v3/ticker/?book='+books[i]
            myjson = {'somekey': 'somevalue'}
            x = requests.post(url, data = myjson)
            y = json.loads(x.text)
            result_dict.append(y['payload'])
        context.update({'cryptos': result_dict})
        return context

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
