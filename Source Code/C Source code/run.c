
/* Metadata Removal Tool v3.5.0 for windows. Compile using gcc c complier mingw only*/
//[ THIS IS A STABLE RELEASE]

#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <stdbool.h>

char file[80], vfile[80], fil[50], vfil[50];

// Function For pausing program temporarily to display message.
void pause(void)
{
  puts("\nPress any key to continue.");
  getc(stdin);
  puts("");
}

//Function to check if output file is generated when expected and throw errors when necessary.
void checker(void)
{
  char eff[80];

  // Guess I should use snprintf here
  memcpy(eff,"exiftool ",10);eff[9]='\0';
  strcat(eff,file);
  strcat(eff,">output.txt");

  int result = system(eff);
  if (result != 0)
  {
      fputs("\n\nOutput.txt couldnot be created!\n" \
            "maybe exiftool is missing or u don't have user permissions or\n"\
            "Something went wrong like you entering a non image file!", stderr);
      exit(EXIT_FAILURE);
  }
}

//Function to check if output file is generated when expected and throw errors when necessary for videos.
void vchecker(void)
{
  int check=0;
  char eff[200] , fvfile[50];
  strcpy(fvfile,"Videos\\final_");
  strcat(fvfile,vfil);
  memcpy(eff,"exiftool ",10);eff[9]='\0';
  strcat(eff,fvfile);
  strcat(eff,">video_output_metadata.txt");
  
  int result = system(eff);
  if (result != 0)
  {
    fputs("\n\nOutput.txt couldnot be created!\n" \
          "maybe exiftool is missing or u don't have user permissions or\n"\
          "Something went wrong like you entering a non image file!", stderr);
    exit(EXIT_FAILURE);
  }
}

//Function to get input from user.
void input(void)
{
  system("cls");
  printf("\n\t┣━━━━━ Image Sanitisation Tool ━━━━━┫\n");
  printf("\n\n Enter Image name:");
  scanf("%30s", fil);
  memcpy(file,"Images\\",8);
  file[8] = '\0';
  strcat(file, fil);
}

bool endswith(char *str, char *extension)
{
  // int i = 0;
  // int j = 0;

  char *last_period = strrchr(str, '.');
  if ((NULL == last_period) || '\0' == *(last_period + 1))
  {
    fprintf(stderr, "ERROR: No extension could be parsed from string '%s'.\n", str);
    exit(EXIT_FAILURE);
  }

  int result = strncasecmp(last_period, extension, 5);
  if (0 != result)
  {
    fprintf(stderr, "ERROR: Unknown image extension '%s'.\n", last_period + 1);
    exit(EXIT_FAILURE);
  }


  // int str1_length = strlen(str);
  // int str2_length = strnlen(extension, 4);
  // if (str1_length > str2_length)
  // {
  //   for(int i = str2_length-1, j=str1_length-1; i>=0;--j,--i)
  //   {
  //     if(tolower(str[j])!= tolower(extension[i]))
  //     {
  //       return false;
  //     }
  //   }
  //   return true;
  // }
  // return false;
  return true;
}

//Function to sanitize the image selected using exiftool.
void sanitize(void)
{
  int check=0;
  int file_length = 0;
  int visit = 0;
  char eff[80];
  char tmp[80];
  file_length = strlen(file);

  if (endswith(file, "tiff") || endswith(file, "tif"))
  {
     memcpy(tmp,"exiftool -all= -CommonIFD0= ",28);tmp[28] = '\0';
     strcat(tmp,file);
     check=system(tmp);
     visit = 1;
  }
 
  else if(visit == 0)
  {
    memcpy(eff,"exiftool ",10);eff[9]='\0';
    strcat(eff,file);
    strcat(eff," -all=");
    check=system(eff);
  }

  if (check != 0)
  {
    fputs("Image sanitisation failed!\n" \
          "maybe exiftool is missing or u don't have user permissions or\n" \
          "Something went wrong like you entering a non image file!", stderr);
    exit(EXIT_FAILURE);
  }
}

//Function to generate and check generation of input log.
void ichecker(void)
{
  char eff[80];
  memcpy(eff,"exiftool ",10);eff[9]='\0';
  strcat(eff,file);
  strcat(eff,">input.txt");

  int check = system(eff);
  if (check != 0)
  {
    fputs("\n\nInput log couldnot be created \n" \
          "maybe exiftool is missing! or u don't have enough access permission!\n" \
          "Something went wrong like you entering a non image file!\n", stderr);
    exit(EXIT_FAILURE);
  }
}


    //Function to generate and check generation of input log for videos.
void ivchecker(void)
{
  char eff[200];
  memcpy(eff,"exiftool ",10);eff[9]='\0';
  strcat(eff,vfile);
  strcat(eff,">video_input_metadata.txt");
  int result = system(eff);
  if(result != 0)
  {

    fputs("\n\nInput log couldnot be created \n" \
          "maybe exiftool is missing! or u don't have enough access permission!\n" \
          "Something went wrong like you entering a non image file!\n", stderr);
    exit(EXIT_FAILURE);
  }
}

//Function to add support for * wildcards.
void detect(void)
{

  bool flag = false;

  unsigned int file_length = strlen(file);

  // Starts at one to skip the first character, which might be a dot
  for (unsigned int i = 1; i < file_length; i++)
  {
    if ((file[i] == '.') && 
        (file[i-1] == '*') && 
        ((file_length - i == 4) || ( file_length - i == 5)))
        {
          flag = true;
          // Should it break here?
          break;
        }

  }

  if (flag)
  {
    FILE *f = fopen(file,"r");
    if (f == NULL)
    {
        fputs("\n\nERROR: FILE NOT FOUND!\n\n", stderr);
        exit(EXIT_FAILURE);
    }
    fclose(f);
  }
}

//Function to check if image file was cleaned successfully by comparing size of input log and output log files generated by exiftool.
int compare(void)
{
  // TODO: Find a way to get file sizes without this
  FILE *input = fopen("input.txt","r");
  FILE *output = fopen("output.txt","r");

  if((input == NULL)||(output == NULL))
  {
      fputs("\n\nEither input.txt or output.txt not found!\n", stderr);
      exit(EXIT_FAILURE);
  }
  fseek(input, 0, SEEK_END);
  fseek(output, 0, SEEK_END);
  unsigned int in_size = ftell(input);
  unsigned int out_size = ftell(output);
  fclose(input);
  fclose(output);
  if(in_size == out_size)
  {
      printf("\n\nNo Significant change!\n");
  }
  else if(in_size > out_size)
  {
      printf("\n\nMetadata Cleaned Successfully!\n");
  }
  // Is this else block actually needed?
  else
  {
      printf("\n\nCleaning done with errors!\n");
  }
  return 0;
}

int run(void) // combine all functions .
{
  input();
  detect();
  ichecker();
  sanitize();
  checker();
  compare();
  return 0;
}

void vinput(void)
{
    /* Gets input ( filename ) for removal  of metadata from videos*/
    system("cls");
    printf("\n\t ┣━━━━━ Video sanitisation tool ━━━━━┫\n");
    printf("\n\n Enter Video name:");
    scanf("%30s",vfil);
        memcpy(vfile,"Videos\\",8);vfile[8]='\0';
        strcat(vfile,vfil);
}

int vdetect(void)
{
  /* Detects if video file is present or not.*/
  // Isn't there a better way of checking if a file exists?
  FILE *f = fopen(vfile, "r");
  if (f == NULL)
  {
      fputs("\n\nERROR: FILE NOT FOUND!", stderr);
      exit(EXIT_FAILURE);
  }

  fclose(f);
  return 0;
}

int vtool(void)
{
  /*Detects ffmpeg in default installation of this software.*/
  // Isn't there a better way of checking if a file exists?
  FILE *f = fopen("ffmpeg.exe", "r");
  if (f==NULL)
  {
    fputs("\n\n Critical Error: FFMPEG.EXE NOT FOUND!", stderr);
    fputs("\n\n┣━━━━━ Video Sanitization Failed! ━━━━━┫\n", stderr);
    exit(EXIT_FAILURE);
  }
  fclose(f);
  return 0;
}

int vsanitise(void)
{
  /* Actual metadata removal process happens here.*/
  // Is this variable used as a stack canary? 
  int status=0;
  char buffer[1000];
  char fvfile[50];
  strcpy(fvfile,"Videos\\final_");
  strcat(fvfile,vfil);
  memcpy(buffer,"ffmpeg -i ",11);
  buffer[10]='\0';
  strcat(buffer,vfile);
  strcat(buffer," -map_metadata -1 -c:v copy -c:a copy ");
  strcat(buffer,fvfile);
  status=system(buffer);

  if (status != 0)
  {
    printf("\n\n     ┣━━━━━ Video Sanitization Failed! ━━━━━┫\n:(\n");
    exit(EXIT_FAILURE);
  }
  return 0;
}

int qrun(void)
{
  /* Responsible for combining all video management functions.*/
  vtool();
  vinput();
  vdetect();
  ivchecker();
  vsanitise();
  vchecker();
  return 0;
}


void menu(void)
{
  // int raw, backdoor;
  // raw = backdoor = 0;

  char choice = 0;

  puts(" ╔═══════════════════════════════════╗ ");
  puts(" ║       Metadata Removal Tool       ║ ");
  puts(" ╚═══════════════════════════════════╝ ");
  puts("");
  puts("");
  puts(" 1 ▸ Sanitize images using exiftool\n");
  puts(" 2 ▸ Sanitize video files using ffmpeg\n");
  puts(" 0 ▸ Exit\n");

  while(1)
  {
    printf("\n Enter your choice (1 or 2):");
  
    choice = getc(stdin);
    puts("");
    
    switch (choice)
    {
      case '1':
        if (run() == 0)
          puts("Done!");
        exit(EXIT_SUCCESS);
      case '2':
        if (qrun() == 0)
          puts("Done!");
        exit(EXIT_SUCCESS);
      case '0':
        puts("Bye!");
        exit(EXIT_SUCCESS);
      default:
        printf("Unknown option '%c'\n", choice);
    }
  }
  //
  //     backdoor = scanf("%d", &raw);
  //     if (backdoor == 1)
  //         break;
  // }
  // if (raw == 1)
  // {
  //     run();
  // }
  // else if( raw== 2)
  // {
  //     qrun();
  //     pause();
  // }
  // else
  // {
  //     pause();
  //     exit(EXIT_SUCCESS);
  // }
}

// Maybe should get some arguments?
int main(void)
{
  // TODO: Find a way to set the title of the window in windows
  // system("title Metadata Removal Tool v3.5.0");


  // Register the pause function so that it won't be necessary to call it each time
  atexit(pause);
  menu();
  exit(EXIT_SUCCESS);
}

