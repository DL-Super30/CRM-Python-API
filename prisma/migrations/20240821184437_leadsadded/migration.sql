-- CreateTable
CREATE TABLE "Lead" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "cc" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "leadStatus" TEXT NOT NULL,
    "leadSource" TEXT NOT NULL,
    "stack" TEXT NOT NULL,
    "course" TEXT NOT NULL,
    "classMode" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "nextFollowUp" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Lead_pkey" PRIMARY KEY ("id")
);
