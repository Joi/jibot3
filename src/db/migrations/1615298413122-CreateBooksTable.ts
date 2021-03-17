import {MigrationInterface, QueryRunner, Table} from "typeorm";
export class CreateBooksTable1615298413122 implements MigrationInterface {
    public async up(queryRunner: QueryRunner): Promise<void> {
        return await queryRunner.createTable(new Table({
            name: "books",
            columns: [
                {
                    name: "id",
                    type: "integer",
                    isPrimary: true,
                    isGenerated: true,
                    generationStrategy: 'increment'
                },
                {
                    name: "title",
                    type: "text",
                    isNullable: false,
                },
                {
                    name: "url",
                    type: "text",
                    isNullable: true,
                    isUnique: true,
                },
                {
                    name: "content",
                    type: "text",
                    isNullable: true,
                },
                ,
                {
                    name: "people",
                    type: "text",
                    isNullable: true
                },
                {
                    name: "places",
                    type: "text",
                    isNullable: true
                },
                {
                    name: "organizations",
                    type: "text",
                    isNullable: true
                }
            ]
        }), true);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        return await queryRunner.dropTable("books");
    }
}
