from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Mailing, Message
from .models import MailingAttempt


class ClientListView(LoginRequiredMixin, ListView):

    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"
    paginate_by = 10

    def get_queryset(self):

        return Client.objects.filter(owner=self.request.user).order_by("-id")


class ClientCreateView(LoginRequiredMixin, CreateView):

    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):

        form.instance.owner = self.request.user
        messages.success(self.request, "Клиент успешно добавлен.")
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):

    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def get_queryset(self):

        return Client.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Клиент успешно обновлён.")
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):

    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Клиент удалён.")
        return super().delete(request, *args, **kwargs)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 10

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Рассылка успешно создана.")
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Рассылка успешно обновлена.")
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Рассылка удалена.")
        return super().delete(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="started").count()
        context["total_clients"] = Client.objects.count()
        return context


class MailingSendView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        mailing.send_mailing()
        messages.success(request, f'Рассылка "{mailing.message.theme}" отправлена.')
        return redirect("mailing:mailing_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user).order_by("-id")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Сообщение успешно создано.")
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно обновлено.")
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Сообщение удалено.")
        return super().delete(request, *args, **kwargs)


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user)
        report = []
        for mailing in mailings:
            attempts = MailingAttempt.objects.filter(mailing=mailing)
            success_count = attempts.filter(status="success").count()
            failure_count = attempts.filter(status="failure").count()
            report.append(
                {
                    "mailing": mailing,
                    "success_count": success_count,
                    "failure_count": failure_count,
                    "total": success_count + failure_count,
                }
            )
        context["report"] = report
        return context
