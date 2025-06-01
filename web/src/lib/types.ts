export type Person = string;
export type Relationship = {
	person1: Person;
	person2: Person;
	context: string;
};

export type User = {
	username: string;
	socials: string;
	degrees_of_separation: string[];
};
