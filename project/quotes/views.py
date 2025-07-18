from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from random import choices
from .models import Quote, Source, SourceType
from .forms import QuoteForm, SourceForm


class RandomQuoteView(View):
    def get(self, request):
        quotes = Quote.objects.all()
        if not quotes:
            return render(request, 'quotes/no_quotes.html')

        weights = [quote.weight for quote in quotes]
        selected_quote = choices(quotes, weights=weights, k=1)[0]

        selected_quote.views += 1
        selected_quote.save()

        return render(request, 'quotes/random_quote.html', {
            'quote': selected_quote,
            'popularity': selected_quote.popularity
        })


class AddQuoteView(View):
    def get(self, request):
        form = QuoteForm()
        return render(request, 'quotes/add_quote.html', {'form': form})

    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
        return render(request, 'quotes/add_quote.html', {'form': form})


class AddSourceView(View):
    def get(self, request):
        form = SourceForm()
        return render(request, 'quotes/add_source.html', {'form': form})

    def post(self, request):
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_quote')
        return render(request, 'quotes/add_source.html', {'form': form})


class LikeDislikeView(View):
    def post(self, request, quote_id, action):
        quote = get_object_or_404(Quote, id=quote_id)
        if action == 'like':
            quote.likes += 1
        elif action == 'dislike':
            quote.dislikes += 1
        quote.save()
        return redirect('random_quote')


class TopQuotesView(ListView):
    model = Quote
    template_name = 'quotes/top_quotes.html'
    context_object_name = 'quotes'
    queryset = Quote.objects.order_by('-likes')[:10]


class SourceListView(ListView):
    model = Source
    template_name = 'quotes/source_list.html'
    context_object_name = 'sources'