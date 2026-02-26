import * as React from "react";

export function Button({ className = "", variant = "solid", ...props }: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "solid" | "outline" | "ghost" }) {
  let base = "px-4 py-2 rounded font-semibold focus:outline-none transition ";
  let variants = {
    solid: "bg-orange-500 text-black hover:bg-orange-600",
    outline: "border border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-black bg-transparent",
    ghost: "bg-transparent hover:bg-neutral-800 text-white"
  };
  return <button className={`${base} ${variants[variant]} ${className}`} {...props} />;
}
