from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from random import choices
from .models import Quote, Source, SourceType
from .forms import QuoteForm, SourceForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RandomQuoteView(View):
    def get(self, request):
        quotes = Quote.objects.all()
        if not quotes:
            return render(request, 'no_quotes.html')

        weights = [quote.weight for quote in quotes]
        selected_quote = choices(quotes, weights=weights, k=1)[0]

        selected_quote.views += 1
        selected_quote.save()

        return render(request, 'random_quote.html', {
            'quote': selected_quote,
            'popularity': selected_quote.popularity,
            'user': request.user
        })


class AddQuoteView(LoginRequiredMixin, View):
    def get(self, request):
        form = QuoteForm(initial={'user': request.user})
        return render(request, 'add_quote.html', {'form': form})

    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.author = request.user
            quote.save()
            return redirect('random_quote')
        return render(request, 'add_quote.html', {'form': form})


class LikeDislikeView(LoginRequiredMixin, View):
    def post(self, request, quote_id, action):
        quote = get_object_or_404(Quote, id=quote_id)
        user = request.user
        referer = request.META.get('HTTP_REFERER')

        if action == 'like':
            if user in quote.dislikes.all():
                quote.dislikes.remove(user)
            quote.likes.add(user)
        elif action == 'dislike':
            if user in quote.likes.all():
                quote.likes.remove(user)
            quote.dislikes.add(user)
        if referer:
            return HttpResponseRedirect(referer)
        return HttpResponseRedirect(reverse('random_quote'))


class TopQuotesView(ListView):
    model = Quote
    template_name = 'top_quotes.html'
    context_object_name = 'quotes'
    queryset = Quote.objects.order_by('-likes')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class SourceListView(ListView):
    model = SourceType
    template_name = 'source_list.html'
    context_object_name = 'source_types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        source_id = self.kwargs.get('source_id')

        if source_id:
            context['current_source'] = get_object_or_404(Source, id=source_id)
            context['quotes'] = context['current_source'].quote_set.all()

        return context

    def get_queryset(self):
        return SourceType.objects.prefetch_related('source_set').all()


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
