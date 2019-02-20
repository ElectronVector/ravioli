from ravioli.strip_comments import strip_comments

def test_multiline_block_comment():
    code = """
            /* See if the handle of the queue being unregistered in actually in the
            registry. */
            for( ux = 0; ux < configQUEUE_REGISTRY_SIZE; ux++ )
            """
    expected = """
            
            for( ux = 0; ux < configQUEUE_REGISTRY_SIZE; ux++ )
            """
    stripped = strip_comments(code)
    assert(stripped == expected)

# def test_some_tricky_code():
#     code = """
#                 /*-----------------------------------------------------------*/
#
#             #if configQUEUE_REGISTRY_SIZE > 0
#
#                 static void vQueueUnregisterQueue( xQueueHandle xQueue )
#                 {
#                 unsigned portBASE_TYPE ux;
#
#                     /* See if the handle of the queue being unregistered in actually in the
#                     registry. */
#                     for( ux = 0; ux < configQUEUE_REGISTRY_SIZE; ux++ )
#                     {
#                         if( xQueueRegistry[ ux ].xHandle == xQueue )
#                         {
#                             /* Set the name to NULL to show that this slot if free again. */
#                             xQueueRegistry[ ux ].pcQueueName = NULL;
#                             break;
#                         }
#                     }
#
#                 }
#
#             #endif
#             """
#     expected = """
#
#
#             #if configQUEUE_REGISTRY_SIZE > 0
#
#                 static void vQueueUnregisterQueue( xQueueHandle xQueue )
#                 {
#                 unsigned portBASE_TYPE ux;
#
#
#                     for( ux = 0; ux < configQUEUE_REGISTRY_SIZE; ux++ )
#                     {
#                         if( xQueueRegistry[ ux ].xHandle == xQueue )
#                         {
#
#                             xQueueRegistry[ ux ].pcQueueName = NULL;
#                             break;
#                         }
#                     }
#
#                 }
#
#             #endif
#             """
#
#     stripped = strip_comments(code)
#     assert(stripped == expected)
