from asgiref import sync

from .django_app.models import Book


async def test_django_tasks(app, django_db):
    @app.task(name="create_book")
    def create_book():
        # Book.objects.create(title="The Old Man and the Sea")
        pass

    # Uncomment when we'll have stopped supporting Python 3.7
    # @app.task(name="create_book_async")
    # async def create_book_async():
    #     await Book.objects.acreate(title="The Async Old Man and the Awaited Sea")

    await create_book.defer_async()
    # await create_book_async.defer_async()

    await app.run_worker_async(wait=False)

    created = await sync.sync_to_async(
        lambda: set(Book.objects.all().values_list("title", flat=True))
    )()

    assert created == {
        "The Old Man and the Sea",
        # "The Async Old Man and the Awaited Sea",
    }
