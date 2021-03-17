export class Book {
    id:		    number;
    title:	    string;
    url:	    string;
    content:    string;
    people:     string;
    places:     string;
    organizations: string;
    constructor(book?:any) {
        return <Book>{
            id:	        (book?.id)      ? book.id       : null,
            title:	    (book?.title)   ? book.title    : null,
            url:	    (book?.url)     ? book.url      : null,
            content:    (book?.content) ? book.content  : null,
            people:     (book?.people)  ? book.people   : null,
            places:     (book?.places)  ? book.places   : null,
            organizations: (book?.organizations) ? book.organizations  : null,
        }
    }
}