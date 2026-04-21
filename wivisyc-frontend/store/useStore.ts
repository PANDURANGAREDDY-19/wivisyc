import { create } from "zustand";

interface Store {
  user: any;
  setUser: (user: any) => void;
}

export const useStore = create<Store>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));