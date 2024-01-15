
/* Metadata Removal Tool v3.5.0 for windows. Compile using gcc c complier mingw only*/
//[ THIS IS A STABLE RELEASE]

#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <stdbool.h>

#define MEMORY_NEEDED 200
#define COMMAND_SZ 400

char file[80], vfile[80], fil[50], vfil[50];

// This global buffer pointer should preferably point to a heap block
char *global_buffer;

// Global installation of required tools?
bool global;
// True if Windows
bool os = false;


// Make sure the global buffer is freed
void free_glbl_buf()
{
  free(global_buffer);
}


#ifdef _WIN32
  // Function For pausing program temporarily to display message.
  // Should only be called in NT systems
  void pause(void)
  {
    puts("\nPress any key to continue.");
    getc(stdin);
    puts("");
  }
#endif


// Function to check if output file is generated when expected and throw errors when necessary for videos.
int vchecker(void)
{
  char *command_buf = malloc(COMMAND_SZ + 1);
  if (NULL == command_buf)
  {
    fputs("Unable to allocate necessary memory. Exiting.", stderr);
    exit(EXIT_FAILURE);
  }

  if (global)
    snprintf(command_buf, COMMAND_SZ, "exiftool 'out_%s' > o.mtd", global_buffer);
  // Windows
  else if (os == true)
    snprintf(command_buf, COMMAND_SZ, ".\\exiftool.exe 'out_%s' > o.mtd", global_buffer);
  else
    snprintf(command_buf, COMMAND_SZ, "./exiftool 'out_%s' > o.mtd", global_buffer);
  
  int return_val = system(command_buf);
  free(command_buf);
  if (return_val != 0)
  {
    fputs("\nUnable to create output log file.\n" \
          "Please check that you have the right permissions.", stderr);
    exit(EXIT_FAILURE);
  }
  return 0;
}


// Function to get input from user.
int input(void)
{
  printf("\n\nEnter path: ");
  fgets(global_buffer, MEMORY_NEEDED, stdin);
  *(strchr(global_buffer, '\n')) = '\0';
  return 0;
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

// Function to sanitize the image selected using exiftool.
int sanitize(void)
{
  char *command_buf = malloc(COMMAND_SZ + 1);
  if (NULL == command_buf)
  {
    fputs("Unable to allocate necessary memory. Exiting", stderr);
    exit(EXIT_FAILURE);
  }

  command_buf[COMMAND_SZ] = '\0';

  char *last_period = strrchr(global_buffer, '.');
  if (NULL == last_period)
  {
    fputs("File has no extension. Exiting.", stderr);
    exit(EXIT_FAILURE);
  }

  char *ends_with = strstr(global_buffer, "tif");
  char *tiff_option = NULL == ends_with ? "" : "-CommonIFD0=";

  if (global)
    snprintf(command_buf, 300, "exiftool -all= %s '%s'", tiff_option, global_buffer);

  // Windows 
  else if (os == true)
    snprintf(command_buf, 300, ".\\exiftool.exe -all= %s '%s'", tiff_option, global_buffer);

  // Linux/MacOS 
  else
    snprintf(command_buf, 300, "./exiftool -all= %s '%s'", tiff_option, global_buffer);


  int return_val = system(command_buf);
  free(command_buf);
  if (return_val != 0)
  {
    fputs("Image sanitization failed!\n" \
          "Please, check your permissions and that the file path is correct.\n", stderr);
    exit(EXIT_FAILURE);
  }
  return 0;
}

// Function to generate and check generation of input log.
int ichecker(char in)
{
  /* WARNING!
   * Using user input like this in a system() call is a big vulnerability!
   * For the Linux/MacOS version, user input should be safely escaped when
   * encasing the path in single quotes '', but I'm not sure the same applies
   * for PowerShell in Windows
   * */
  char *command_buf = malloc(COMMAND_SZ + 1);
  if (NULL == command_buf)
  {
    fputs("Unable to allocate necessary memory. Exiting", stderr);
    exit(EXIT_FAILURE);
  }
  command_buf[COMMAND_SZ] = '\0';

  if (global)
    snprintf(command_buf, 300, "exiftool '%s' > %c.mtd", global_buffer, in);

  // Windows
  else if (os == true)
    snprintf(command_buf, 300, "./exiftool.exe '%s' > %c.mtd", global_buffer, in);

  // Linux/MacOS
  else
    snprintf(command_buf, 300, "./exiftool '%s' > %c.mtd", global_buffer, in);

  int return_val = system(command_buf);
  free(command_buf);

  if (return_val != 0)
  {
    fputs("\n\nInput log couldn't be created.\n" \
          "Please, check that you have the right permissions and that\n" \
          "the file exists.\n", 
          stderr);
    exit(EXIT_FAILURE);
  }
  return 0;
}


// Function to check if the file was cleaned successfully
int compare(void)
{
  // TODO: Find a way to get file sizes without this
  FILE *input = fopen("i.mtd","r");
  if (NULL == input)
  {
    fputs("Unable to open required file 'i.mtd' in current directory.", stderr);
    exit(EXIT_FAILURE);
  }

  FILE *output = fopen("o.mtd","r");
  if (NULL == output)
  {
    fputs("Unable to open required file 'o.mtd' in current directory.", stderr);
    exit(EXIT_FAILURE);
  }

  fseek(input, 0, SEEK_END);
  unsigned int in_size = ftell(input);
  fclose(input);

  fseek(output, 0, SEEK_END);
  unsigned int out_size = ftell(output);
  fclose(output);


  if (in_size > out_size)
  {
      puts("\nMetadata cleaned successfully!");
  }
  else 
  {
      puts("\nNo significant change!");
  }

  // Remove log files
  system("rm i.mtd o.mtd");
  return 0;
}


// Check for exiftool
int tool(void)
{
  if (system("exiftool -ver > nothing") == 0)
    global = true;

  /* Windows */
  else if (system("./exiftool.exe -ver > nothing") == 0 && os)
    global = false;

  /* Linux/MacOS */
  else if (system("./exiftool -ver > nothing") == 0 && os == false)
    global = false;

  else 
  {
    fputs("\n\n Critical Error: exiftool NOT FOUND!", stderr);
    fputs("\n\n┣━━━━━ Image Sanitization Failed! ━━━━━┫\n", stderr);
    exit(EXIT_FAILURE);
  }

  system("rm nothing");
  return 0;
}


// Check for ffmpeg
int vtool(void)
{
  if (system("ffmpeg -version > nothing") == 0)
    global = true;

  /* Windows */
  else if (system(".\\ffmpeg.exe -version > nothing") == 0 && os)
    global = false;

  /* Linux/MacOS */
  else if (system("./ffmpeg -version > nothing") == 0 && os == false)
    global = false;

  else 
  {
    fputs("\n\n Critical Error: ffmpeg NOT FOUND!", stderr);
    fputs("\n\n┣━━━━━ Video Sanitization Failed! ━━━━━┫\n", stderr);
    exit(EXIT_FAILURE);
  }

  system("rm nothing");
  return 0;
}


int vsanitize(void)
{
  char *command_buf = malloc(COMMAND_SZ + 1);
  if (NULL == command_buf)
  {
    fputs("Unable to allocate necessary memory. Exiting.", stderr);
    exit(EXIT_FAILURE);
  }

  if (global)
    snprintf(command_buf, COMMAND_SZ, "ffmpeg -i '%s' -map_metadata -1 -c:v copy -c:a copy 'out_%s'", global_buffer, global_buffer);
  // Windows 
  else if (os == true)
    snprintf(command_buf, COMMAND_SZ, ".\\ffmpeg.exe -i '%s' -map_metadata -1 -c:v copy -c:a copy 'out_%s'", global_buffer, global_buffer);
  else
    snprintf(command_buf, COMMAND_SZ, "./ffmpeg -i '%s' -map_metadata -1 -c:v copy -c:a copy 'out_%s'", global_buffer, global_buffer);


  int return_val = system(command_buf);
  free(command_buf);
  if (return_val != 0)
  {
    fputs("\n\n     ┣━━━━━ Video Sanitization Failed! ━━━━━┫", stderr);
    exit(EXIT_FAILURE);
  }
  return 0;
}


// Combine video functions
int qrun(void)
{
  // Check for ffmpeg
  vtool();
  puts("\n\t ┣━━━━━ Video sanitization tool ━━━━━┫\n");
  input();
  ichecker('i');
  // Why are images sanitized in-place but videos are not?
  vsanitize();
  vchecker();
  compare();
  return 0;
}


// Combine image functions
int run(void) 
{
  // Check exiftool
  tool();
  // Get image path 
  puts("\n\t┣━━━━━ Image Sanitisation Tool ━━━━━┫");
  input();
  // Get input metadata (might not be completely sanitized)
  ichecker('i');
  // Run some exiftool commands to delete the metadata
  sanitize();
  // Get output metadata
  ichecker('o');
  // Compare sizes of files 
  compare();
  return 0;
}


void menu(void)
{
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
    printf("\n Enter your choice (1, 2 or 0):");
  
    choice = getc(stdin);
    // Consume newline
    getc(stdin);
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
}

// Maybe should get some arguments? Chat me up if adding command-line options
// for power users sounds like a good idea
int main(void)
{
  global_buffer = malloc(MEMORY_NEEDED + 1);
  if (NULL == global_buffer)
  {
    fputs("Could not allocate enough memory to operate. Exiting.\n", stderr);
    exit(EXIT_FAILURE);
  }

  global_buffer[MEMORY_NEEDED] = '\0';

  atexit(free_glbl_buf);

  // TODO: Test this in Windows
  #ifdef _WIN32
  os = true;
  system("title Metadata Removal Tool v3.5.0");
  atexit(pause);
  #endif

  menu();
  exit(EXIT_SUCCESS);
}

