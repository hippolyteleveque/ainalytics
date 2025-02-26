import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

type User = {
  email?: string;
  accessToken?: string;
};

type Account = {
  provider?: string;
  id_token?: string;
};

type Token = {
  accessToken?: string;
};

type Session = {
  accessToken?: string;
};

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    }),
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // Check if the user exists in your database
        if (!credentials?.email || !credentials?.password) {
          return null;
        }
        const response = await loginUser(
          credentials?.email,
          credentials?.password
        );

        // Return the user object (without the password)
        return {
          id: response.user_id,
          email: response.email,
          accessToken: response.access_token,
        };
      },
    }),
  ],
  callbacks: {
    async signIn({ user, account }: { user: User; account?: Account }) {
      if (account?.provider === "google") {
        const response = await fetch("http://localhost:8000/auth/google", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: user.email,
            token: account.id_token,
          }),
        });

        if (!response.ok) {
          return false;
        }
        const resp = await response.json();
        user.accessToken = resp.access_token;
        return true;
      }
      // For our own provider we directly allows the auth
      return true;
    },
    async jwt({ token, user }: { token: Token; user: User }) {
      // Attach the user ID to the JWT token
      if (user) {
        token.accessToken = user.accessToken;
      }
      return token;
    },
    async session({ token, session }: { token: Token; session: Session }) {
      session.accessToken = token.accessToken;
      return session;
    },
  },
};

const loginUser = async (email: string, password: string) => {
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);
  const response = await fetch("http://localhost:8000/auth/login", {
    method: "POST",
    body: formData,
  });

  const user = await response.json();
  return user;
};
