from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .models import Birthday
from .utils import calculate_birthday_countdown


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context)


def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(
        request.POST or None,
        # Файлы, переданные в запросе, указываются отдельно.
        files=request.FILES or None,
        instance=instance
        )
    # Остальной код без изменений.
    # Если форма валидна...
    context = {'form': form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    # Получаем список всех объектов с сортировкой по id.
    birthdays = Birthday.objects.order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страницу.
    paginator = Paginator(birthdays, 10)

    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')
    # Получаем запрошенную страницу пагинатора.
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)
    # Вместо полного списка объектов передаём в контекст
    # объект страницы пагинатора
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)
