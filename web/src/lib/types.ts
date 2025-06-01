export type Person = {
	name: string;
	publicBio: string;
	privateBio: string;
};
export type Relationship = {
	person1: Person;
	person2: Person;
	level: string;
};

export type User = {
	username: string;
	socials: string;
	degrees_of_separation: number;
};
