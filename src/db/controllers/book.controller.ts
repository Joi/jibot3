import { getRepository } from "typeorm";
import { NextFunction, Request, Response } from "express";
import { Book } from "../entities/book";
export class BookController {
    private bookRepository = getRepository(Book);
	async all(request: Request, response: Response, next: NextFunction) {
        return this.bookRepository.find();
    }
    async one(request: Request, response: Response, next: NextFunction) {
        return this.bookRepository.findOne(request.params.id);
    }
    async save(request: Request, response: Response, next: NextFunction) {
		await this.bookRepository.save(request.body);
		return this.bookRepository.find();
    }
    async remove(request: Request, response: Response, next: NextFunction) {
        const bookToRemove = await this.bookRepository.findOne(request.params.id);
        await this.bookRepository.remove(bookToRemove);
		return this.bookRepository.find();
    }
}