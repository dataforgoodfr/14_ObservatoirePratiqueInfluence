FROM node:24-slim AS base
ENV PNPM_HOME=/usr/local/bin
ENV PATH="$PNPM_HOME:$PATH"
COPY . /app
WORKDIR /app

RUN SHELL="$(which bash)" npx pnpm@latest-10 dlx @pnpm/exe@latest-10 setup

FROM base AS prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM base AS build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

FROM base
COPY --from=prod-deps /app/node_modules /app/node_modules
COPY --from=build /app/.next /app/.next
EXPOSE 3000
CMD [ "pnpm", "start" ]
