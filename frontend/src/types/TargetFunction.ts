export interface TargetFunction {
    param_name: string,
    display_name: string,
    description: string
}

export const availableTargetFunctions: TargetFunction[] = [
  {
    param_name: "minremoney",
    display_name: "Minimalize Remaining Money",
    description: "Spend as much of your budget as possible, leaving the least amount of unused money."
  },
  {
    param_name: "maxcandy",
    display_name: "Maximize Candy",
    description: "Buy as many items as possible, maximizing the number of purchased products regardless of leftover money."
  }
];
