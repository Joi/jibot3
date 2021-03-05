export class Book {
    id:		number;
    title:	string;
    url:	string;
    constructor(book?:any) {
        return <Book>{
            id:	    (book?.id)     ? book.id     : null,
            title:	(book?.title)  ? book.title  : null,
            url:	(book?.url)    ? book.url    : null
        }
    }
}