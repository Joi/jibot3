export class Option {
    id:		number;
    name:	string;
    value:	string;
    constructor(option?:any) {
        return <Option>{
            id:	    (option?.id)     ? option.id     : null,
            name:	(option?.name)  ? option.name  : null,
            value:	(option?.value)    ? option.value    : null
        }
    }
}